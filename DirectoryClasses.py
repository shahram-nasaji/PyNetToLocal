import os
import shutil

class DirectorySvc:
	def __init__(self):
		self.sub_directories = []

	def get_directories(self,root_directory):
		try:
			directories = os.listdir(root_directory)

			for directory in directories:
				full_directory_path = os.path.join(root_directory, directory)

				if (os.path.isdir(full_directory_path)):
					self.sub_directories.append(full_directory_path)
					self.get_directories(full_directory_path)

			return self.sub_directories
		except PermissionError as error:
			pass

	def get_files(self, root_directory):
		try:
			files = []
			directories = os.listdir(root_directory)

			for directory in directories:
				full_directory_path = os.path.join(root_directory, directory)

				if (os.path.isdir(full_directory_path) == False):
					files.append(full_directory_path)

			return files
		except PermissionError as error:
			pass

	def exist_directory(self,full_diretory_path):
		try:
			return os.path.isdir(full_diretory_path)
		except Exception as error:
			print(error)

	def make_directory(self,full_diretory_path):
		try:
			if (self.exist_directory(full_diretory_path) == False):
				os.makedirs(full_diretory_path)
				return True
			return False
		except Exception as error:
			print(error)

	def replicate_directories(self, source_directory, destination_directory):
		source_sub_directories = self.get_directories(source_directory)

		for source_sub_directory in source_sub_directories:
			final_destination_directory = destination_directory + source_sub_directory[len(source_directory):]
			self.make_directory(final_destination_directory)

			files = self.get_files(source_sub_directory)
			for source_file in files:
				destination_file = final_destination_directory + source_file[len(source_sub_directory):]

				if (os.path.isfile(destination_file) == False):
					shutil.copy2(source_file, final_destination_directory)