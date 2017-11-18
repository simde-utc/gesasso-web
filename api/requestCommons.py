class RequestResult:
	success = False
	content = None      # should be != None if success
	errorName = ""  # 'MISSING_PARAMETER'
	errorMessage = ""   # 'At least one of the parameter is missing'
	errorDetails = ""   # 'This route expects the following parameters: [...]'

	def __init__(self, success, content = None, raw = None, errorName = "None", errorMessage = "None", errorDetails = ""):
		self.success = success
		self.content = content
		self.errorName = errorName
		self.errorMessage = errorMessage
		self.errorDetails = errorDetails
		self.raw = raw