

class awsKeyProvider():

    def coordinates_file_key(self, mhc_class:str, pdb_code:str, assembly_id:str, coordinates_type:str, solvent:str, format:str, privacy:str='public') -> str:
        """
        Function to return the S3 key for a specific coordinates file

        Args:
            pdb_code (str): the pdb code of the structure e.g. '7ejn'
            coordinates_type (str): the part of the structure e.g. 'raw', 'aligned', 'peptide', 'abd'
            privacy (str): whether the file is public or private (not yet used)


        Returns:
            str : the S3 key for the object
        """
        key = f'files/{privacy.lower()}/{mhc_class.lower()}/{solvent.lower()}/{coordinates_type.lower()}/{pdb_code.lower()}_{assembly_id}.{format.lower()}'
        return key
