from . import commands
import taskathon
import arrow

class TwRun(commands.BaseCommand):
	def __init__(self, host):
		super().__init__(host)
		self.addListener("tw")
		self.addListener("taskw")
		self.addListener("taskwarrior")
		self.inter = True
		self.tw = taskathon.Tasks(self.cfg._get('debug', False))
		
	def onTrigger(self, value):
		out = self.tw.cmd(value)
		return self.output(f"\n{out}")	
	
class TwDOM(commands.BaseCommand):
	def __init__(self, host):
		super().__init__(host)
		self.addListener("tdom")
		self.inter = True
		self.tw = taskathon.Tasks(self.cfg._get('debug', False))
		
	def onTrigger(self, value):
		out = self.tw.get(value)
		return self.output(out)	
	
class Twls(commands.BaseCommand):
	def __init__(self, host):
		super().__init__(host)
		self.addListener("list tasks")
		self.tw = taskathon.Tasks(self.cfg._get('debug', False))
		
	def onTrigger(self):
		out = self.tw.export()
		s = "\n"
		for item in out:
			if item['status'] == "pending":
				pro = ""
				if item.get('project', None):
					pro += f"[{item['project']}] "
					
				
				created = arrow.get(item['entry'], 'YYYYMMDD')
				modified = arrow.get(item['modified'], 'YYYYMMDD')
				
				dt = f"- Created on {created.day}/{created.month}/{created.year}"
				if created != modified:
					dt += f" (Modified on {modified.day}/{modified.month}/{modified.year})"
				s += f" {item['id']}: {pro}{item['description']} {dt}\n"
				
		return self.output(s)	
	
class TwGetTask(commands.BaseCommand):
	def __init__(self, host):
		super().__init__(host)
		self.addListener("show task")
		self.inter = True
		self.tw = taskathon.Tasks(self.cfg._get('debug', False))
		
	def onTrigger(self, value):
		try:
			item = self.tw.export(value)[0]
		except:
			return self.message("Problem finding that task.")
		s = ""
		if item['status'] == "pending":
			pro = ""
			if item.get('project', None):
				pro += f"[{item['project']}] "
				
			
			created = arrow.get(item['entry'], 'YYYYMMDD')
			modified = arrow.get(item['modified'], 'YYYYMMDD')
			
			dt = f"- Created on {created.day}/{created.month}/{created.year}"
			if created != modified:
				dt += f" (Modified on {modified.day}/{modified.month}/{modified.year})"
			s += f" {item['id']}: {pro}{item['description']} {dt}"
			
		return self.output(s)	
	
class AddTaskwPrompt(commands.BaseCommand):
	def __init__(self, host):
		super().__init__(host)
		self.addListener("add a task", 100)
		self.addListener("add new task", 95)
		self.addListener("create task", 95)
		self.tw = taskathon.Tasks(self.cfg._get('debug', False))
		
	def onTrigger(self):
		return self.hold("What should I write?")
	
	def onHeld(self, value):
		if value == "":
			return self.message("Cancelled.")
		
		self.tw.add(value)
		return self.message("Task added.")

class AddTaskw(commands.BaseCommand):
	def __init__(self, host):
		super().__init__(host)
		self.addListener("add task")
		self.inter = True
		self.tw = taskathon.Tasks(self.cfg._get('debug', False))
		
	def onTrigger(self, value):
		self.tw.add(value)
		return self.message("Task added.")	

	
