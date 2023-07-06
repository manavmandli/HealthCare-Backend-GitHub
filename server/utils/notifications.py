from notifications_app.models import NotificationModel

notification_actions = {
    "job_posted": "A new job has been posted!", 
    # "new_job_application": "You have a new application for {job_name}",
    # "accept_hiring_offer": "{provider_name} accepted your job offer!", 
    # "reject_hiring_offer": "{provider_name} rejected your job offer!",
    # "job_completed": "{job_name} has been marked as complete by the facility!",
    # "job_cancelled": "{job_name} has been cancelled by the facility!",
    "new_job_application": "You have a new application for {0}",
    "new_hiring_offer": "{0} has sent you a job offer!", 
    "accept_hiring_offer": "{0} accepted your job offer!", 
    "reject_hiring_offer": "{0} rejected your job offer!",
    "job_completed": "{0} has been marked as complete by the facility!",
    "job_cancelled": "{0} has been cancelled by the facility!",
}

def get_notification_message_template(action):
    if action in notification_actions:
        return notification_actions.get(action) 
    else:
        return None

def send_notification(receiver=None, action=None, context=[]):
    if receiver is not None:
        message_template = get_notification_message_template(action)
        if message_template is not None:
            message_content = message_template.format(*context)
            
            created = []
            for user in receiver:
                notification = NotificationModel.objects.create(content=message_content)
                notification.reciever.add(user)
                created.append(notification)
            
            if created:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
    
