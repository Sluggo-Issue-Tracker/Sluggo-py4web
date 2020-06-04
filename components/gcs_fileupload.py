import base64
import datetime
import time
import urllib.parse
import uuid

# If these packages are not found, install pycrypto.
# You may need to add this to the requirements.txt
import Crypto.Hash.SHA256 as SHA256
import Crypto.PublicKey.RSA as RSA
import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5

from py4web import action, URL, request
from yatl.helpers import XML
from py4web.utils.url_signer import URLSigner
from py4web.core import Fixture

def base64sign(plaintext, private_key):
    """Function used to sign the URLs."""
    shahash = SHA256.new(plaintext.encode('utf8'))
    signer = PKCS1_v1_5.new(private_key)
    signature_bytes = signer.sign(shahash)
    return base64.b64encode(signature_bytes)

GCS_API_ENDPOINT = 'https://storage.googleapis.com'

SIGNATURE_STRING = ('{verb}\n'
                    '{content_md5}\n'
                    '{content_type}\n'
                    '{expiration}\n'
                    '{resource}')


def sign_url(path, expiration, account_email, keytext,
             verb='GET', content_type='', content_md5=''):
    """
    Forms and returns the full signed URL to access GCS.
    path: is the name of the GCS file to sign
    expiration: is a datetime object
    account_email: is the email of the account performing isgnature
    keytext: is the key to use for signing (assigned by google)
    verb: only 'GET' supported
    content_type: optional
    content_md5: also optional
    """
    private_key = RSA.importKey(keytext)
    if not path.startswith('/'):
        path = '/'+path
    base_url = '%s%s' % (GCS_API_ENDPOINT, path)
    string_to_sign = SIGNATURE_STRING.format(verb=verb,
                                             content_md5=content_md5,
                                             content_type=content_type,
                                             expiration=expiration,
                                             resource=path)
    print("string to sign:", string_to_sign)
    signature_signed = base64sign(string_to_sign, private_key)
    query_params = {'GoogleAccessId': account_email,
                    'Expires': str(expiration),
                    'Signature': signature_signed}
    return base_url+'?'+urllib.parse.urlencode(query_params)


def gcs_url(keys, path, verb='GET', expiration_secs=1000, content_type=''):
    """Generates a signed URL for GCS.
    :param keys: keys to GCS.
    :param path: path to sign.
    :param verb: action to be allowed (GET, PUT, etc)
    :param expiration_secs: expiration time for URL
    :param content_type: content type, to limit what can be uploaded.
    """
    expiration = int(time.time() + expiration_secs)
    signed_url = sign_url(path, verb=verb, expiration = expiration,
                          content_type=content_type,
                          account_email=keys['client_email'],
                          keytext=keys['private_key']
                          )
    return signed_url


class GCSFileUpload(Fixture):

    GCS_FILE_UPLOAD = ('<gcsfileupload '
                       'callback_url="{callback_url}" '
                       'obtain_gcs_url="{obtain_gcs_url}" '
                       'notify_url="{notify_url}" '
                       'delete_url="{delete_url}" '
                       '@download_url="download_urlSet"></gcsfileupload>')

    def __init__(self, url, bucket, gcs_keys, session,
                 signer=None, db=None, auth=None,
                 writable=True, deletable=True):
        """
        File uploader to GCS.
        :param url: URL to use to communicate to the server that the upload has occurred.
        :param bucket: GCS bucket where to put the files.
        :param gcs_keys: GCS keys used for signing the upload.
        :param session: session, used to sign the URL.
        :param signer: a URL signer.  Can be left to None.
        :param db: database; use it if the on_upload methods needs to write to the db.
        :param auth: use it if the on_upload method needs the auth.
        :param writable: Accepts uploads.
        :param deletable: Can be deleted.
        """
        self.obtain_gcs_url = url + '/obtain'
        self.callback_url = url + '/callback'
        self.notify_url = url + '/notify'
        self.delete_url = url + '/delete'
        assert bucket.startswith('/') and bucket.endswith('/')
        self.bucket = bucket
        self.gcs_keys = gcs_keys
        self.signer = signer or URLSigner(session)
        self.session = session
        self.writable = writable
        self.deletable = deletable
        # Creates an action (an entry point for URL calls),
        # mapped to the api method, that can be used to request pages
        # for the table.
        self.__prerequisites__ = [session]
        args = list(filter(None, [session, db, auth, self.signer.verify()]))
        # Registers the callback URL.
        f = action.uses(*args)(self.load)
        action(self.callback_url + "/<id>", method=["GET"])(f)
        # Registers the URL to obtain an upload URL.
        f = action.uses(*args)(self.obtain_url)
        action(self.obtain_gcs_url + "/<id>", method=["POST"])(f)
        # Registers the notification URL, which will be called once the upload
        # is complete.
        f = action.uses(*args)(self.notify_upload)
        action(self.notify_url + "/<id>", method=["POST"])(f)
        # Registers the URL to delete a previous file.
        f = action.uses(*args)(self.notify_delete)
        action(self.delete_url + "/<id>", method=["POST"])(f)

    def __call__(self, id=None):
        """This method returns the element that can be included in the page.
        :param id: id of the file uploaded.  This can be useful if there are
        multiple instances of this uploader on the page.
        """
        return XML(GCSFileUpload.GCS_FILE_UPLOAD.format(
            callback_url=URL(self.callback_url, id, signer=self.signer),
            obtain_gcs_url=URL(self.obtain_gcs_url, id, signer=self.signer),
            notify_url=URL(self.notify_url, id, signer=self.signer),
            delete_url=URL(self.delete_url, id, signer=self.signer),
        ))

    def load(self, id=None):
        """Returns the data to initially set up the upload."""
        if self.session.get('gcs_fileupload') is None:
            self.session['gcs_fileupload'] = {}
            # self.session.was_modified()
        return self._return_file_info(id)

    def obtain_url(self, id=None):
        """Returns the upload URL for GCS."""
        action = request.json.get("action")
        if action == "PUT":
            mimetype = request.json.get("mimetype", "")
            path = self.bucket + str(uuid.uuid4())
            print("Obtain url for", path, mimetype)
            upload_url = gcs_url(self.gcs_keys, path, verb='PUT',
                                 content_type=mimetype)
            return dict(signed_url=upload_url, path=path)
        elif action == "DELETE":
            file_id = request.json.get("file_id")
            delete_url = None
            if file_id is not None:
                delete_url = gcs_url(self.gcs_keys, file_id, verb='DELETE')
            return dict(signed_url=delete_url)

    def notify_upload(self, id=None):
        """We get the notification that the file has been uploaded.
        Needs to be implemented in subclassing.
        """
        file_type = request.json.get("file_type")
        file_name = request.json.get("file_name")
        file_path = request.json.get("file_path")
        print("File was uploaded:", file_path, file_name, file_type)
        if self.session.get('gcs_fileupload') is None:
            self.session['gcs_fileupload'] = {}
        d = self.session['gcs_fileupload'].get(id, {})
        d['file_path'] = file_path
        d['file_name'] = file_name
        d['file_date'] = datetime.datetime.utcnow().isoformat()
        d['file_id'] = file_path # For simplicity.
        self.session['gcs_fileupload'][id] = d
        # self.session.was_modified()
        return self._return_file_info(id)

    def notify_delete(self, id=None):
        """Deletes the previously uploaded file, if any."""
        self.session['gcs_fileupload'][id] = {}
        # self.session.was_modified()
        return self._return_file_info(id)

    def _return_file_info(self, id):
        """Returns the information for the current file."""
        d = self.session['gcs_fileupload'].get(id, {})
        download_url=None,
        if d.get('file_path') is not None:
            download_url = gcs_url(self.gcs_keys, d.get('file_path'), verb='GET')
        r = dict(
            file_name=d.get('file_name'),
            file_date=d.get('file_date'),
            file_id=d.get('file_id'),
            deletable=self.deletable,
            writable=self.writable,
            download_url=download_url,
        )
        print("Returned:", r)
        return r


