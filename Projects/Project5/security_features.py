import os
import json
import time
from datetime import datetime, timedelta
import hashlib

class SecurityFeatures:
    def __init__(self):
        self.metadata_extension = ".meta"
        
    def encrypt_with_security(self, file_path, encrypted_content, expiry_hours=None, 
                            max_attempts=None, fake_password=None, fake_content=None):
      
       
        with open(file_path, 'w') as f:
            f.write(encrypted_content)
        
      
        metadata = {
            'created_at': time.time(),
            'attempts_left': max_attempts if max_attempts is not None else -1,  
            'expiry_time': time.time() + (expiry_hours * 3600) if expiry_hours else None,
            'fake_password_hash': self._hash_password(fake_password) if fake_password else None,
            'has_fake_content': bool(fake_content)
        }
        
       
        if fake_content:
            fake_file = file_path + '.fake'
            with open(fake_file, 'w') as f:
                f.write(fake_content)
        
       
        metadata_file = file_path + self.metadata_extension
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f)
             
    def check_security(self, file_path, password=None):
       
        metadata_file = file_path + self.metadata_extension
        
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        except FileNotFoundError:
            return True, False, "No security metadata found"
            
       
        if metadata.get('expiry_time'):
            if time.time() > metadata['expiry_time']:
                self._delete_files(file_path)
                return False, False, "File has expired and been deleted"
                
       
        if metadata.get('attempts_left') is not None:
            if metadata['attempts_left'] == -1:  
                pass
            elif metadata['attempts_left'] <= 0:
                self._delete_files(file_path)
                return False, False, "Maximum attempts exceeded, file deleted"
            else:
                metadata['attempts_left'] -= 1
                self._save_metadata(metadata_file, metadata)
                
       
        if password and metadata.get('fake_password_hash'):
            if self._hash_password(password) == metadata['fake_password_hash']:
                if metadata.get('has_fake_content'):
                    return True, True, "Accessing fake content"
                return False, False, "Invalid password"
                
        attempts_msg = ""
        if metadata.get('attempts_left') is not None and metadata['attempts_left'] != -1:
            attempts_msg = f"Attempts left: {metadata['attempts_left']}"
        
        return True, False, attempts_msg
    
    def _hash_password(self, password):
        if not password:
            return None
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _save_metadata(self, metadata_file, metadata):
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f)
        
    def _delete_files(self, base_file_path):
      
        files_to_delete = [
            base_file_path,
            base_file_path + self.metadata_extension,
            base_file_path + '.fake'
        ]
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
            except FileNotFoundError:
                pass

    def get_file_info(self, file_path):
       
        try:
            with open(file_path + self.metadata_extension, 'r') as f:
                metadata = json.load(f)
                
            info = []
            if metadata.get('expiry_time'):
                expiry_date = datetime.fromtimestamp(metadata['expiry_time'])
                info.append(f"Expires: {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if metadata.get('attempts_left') is not None:
                if metadata['attempts_left'] == -1:
                    info.append("Unlimited attempts")
                else:
                    info.append(f"Attempts left: {metadata['attempts_left']}")
                
            if metadata.get('fake_password_hash'):
                info.append("Has fake password protection")
                
            return "\n".join(info) if info else "No security features enabled"
        except FileNotFoundError:
            return "No security metadata found" 