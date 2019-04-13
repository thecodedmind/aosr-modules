from . import commands 
import random

class DuckDuckGo(commands.BaseCommand):
	def __init__(self, host):
		super().__init__(host)
		
		try:
			import duckduckgo
			self.client = duckduckgo.DDG('AOSR')
			
		except Exception as e:
			print(e)
			print("DDG API not available. Download from http://github.com/codedthoughts/duckduckgo")
			self.disabled = True
			
		self.addListener("ddg")
		self.addListener("search for ")
		self.inter = True
	
	def doSearch(self, value):
		if value.endswith("--"):
			data = self.client.search(value[:-2])
			s = ""
			for i in range(0, 10):
				f = True
				s += f"{data['snippets'][i]}\nhttp://{data['urls'][i]}\n\n"
			
			if s != "":
				return s
			else:
				return "No results found."
				
			num = -1
			for i in range(0, 10):
				if f'/{i}' in value:
					value = value.replace(f'/{i}', '')
					num = i
			
			if num == -1:
				num = random.randint(0, 10)

			data = self.client.search(value)
			
			#print(data['snippets'][num])
			#print(data['urls'][num])
			return f"{self.host.formatting.Bold}[Search for {value} (RESULT: {num})]{self.host.reset_f}\n{data['snippets'][num]}\nhttp://{data['urls'][num]}"
	
	def onHeld(self, value):
		return self.output(self.doSearch(value))
	
	def onTrigger(self, value = ""):
		if self.disabled:
			return self.message("DDG API not available. Download from http://github.com/codedthoughts/duckduckgo")
		
		if value == "":
			return self.hold("Search for what?")
		return self.output(self.doSearch(value))
