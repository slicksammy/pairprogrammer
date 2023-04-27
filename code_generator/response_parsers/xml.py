import re
import json
from lxml import etree

class Xml:
    @classmethod
    def response_prompt(cls):
        """
        Use the following format for your response:
                
        <RESPONSE>
            <COMMAND>create_file</COMMAND>
            <ARGUMENTS>{"file_path": "some/file_path.rb"}</ARGUMENTS> // If there are no arguments, use an empty JSON object: {}
            <EXPLANATION>I need to create a new file</EXPLANATION>
            <SUMMARY>creating a file</SUMMARY>
            <TASK>the task you are working on</TASK>
        </RESPONSE>
        
        All fields are required
        """
    
    @classmethod
    def parse_response_object(cls, response):
        match = re.search(r'<RESPONSE>.*<\/RESPONSE>', response, re.MULTILINE)
        return match.group(0) if match else None
    
    def parse_object_to_dict(cls, object):
        root = etree.fromstring(object)
        arguments = json.loads(root.findtext('ARGUMENTS', '{}'))

        return {
            'command': root.findtext('COMMAND'),
            'arguments': arguments,
            'explanation': root.findtext('EXPLANATION'),
            'summary': root.findtext('SUMMARY'),
            'task': root.findtext('TASK')
        }