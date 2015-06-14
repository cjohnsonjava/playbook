from pygithub3 import Github
from ...utils.configHelper import getConfig
import logging

logger = logging.getLogger('playbook')

def createAcceptIssue(milestoneNumber, milestoneRepo):
        title = 'Accept the story (milestone)'
        descr = ('The product owner should complete this task after all the '
                 'acceptance criteria are met for this story (milestone).')
        issue = Issue(None, 
                      title, 
                      descr, 
                      None, 
                      milestoneNumber, 
                      None, 
                      milestoneRepo)
        logger.info("Creating Accept Issue related to milestone #%d" +
                    " into repository %s", 
                    milestoneNumber, milestoneRepo)
        return (issue, issue.create())
        
class Issue(object):
    
    def __init__(self, id, title, body, assignee, milestoneNumber, labels, repo):
        
        token = getConfig("github.token")
        owner = getConfig("github.owner")
        
        self.__gh = Github(token=token, user=owner, repo=repo)
        self.__id = id
        self.__title = title
        self.__body = body
        self.__assignee = assignee
        self.__milestoneNumber = milestoneNumber
        self.__labels = labels
        self.__repo = repo
        
    def create(self):
        if self.__title is None:
            logger.error("Title is a required field. This issue will not" +
                         " be exported to GitHub: %s", self.__dict__)
            #TODO: throw exception!?!?!?!
            return
        
        data = { 'title': self.__title }
            
        if self.__body is not None:
            data['body'] = self.__body
            
        if self.__assignee is not None:
            data['assignee'] = self.__assignee
            
        if self.__milestoneNumber is not None:
            data['milestone'] = self.__milestoneNumber
            
        if self.__labels is not None:
            data['labels'] = self.__labels
            
        try:
            ghIssue = self.__gh.issues.create(data)
            logger.info("Issue exported to GitHub: %s", data)
            return ghIssue.number
        except Exception:
            logger.exception("Error exporting issue to GitHub: %s", data)
            return None

    def getId(self):
        return self.__id
                
    def getTitle(self):
        return self.__title
    
    def getBody(self):
        return self.__body
        
    def getAssignee(self):
        return self.__assignee
        
    def getmilestoneNumber(self):
        return self.__milestoneNumber
        
    def getLabels(self):
        return self.__labels

    def getGitHub(self):
        return self.__gh
    
    def setGitHub(self, gitHub):
        self.__gh = gitHub
        
        