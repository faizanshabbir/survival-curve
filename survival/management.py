from django.db.models import signals
from django.contrib.auth.models import Group, Permission
import models 

#FOR A SUBSCRIBER USER, IT IS MORE DIFFICULT BECAUSE A BASIC USER REQUIRES A PASSWORD
# Primary user attributes: username, password, email, first_name, last_name

#myappname_group_permissions = {
#  "Basic_User": [
#    ],
#  "Paid_User": [
#    ],
#}

#def create_user_groups(app, created_models, verbosity, **kwargs):
#  if verbosity>0:
#    print "Initialising data post_syncdb"
#  for group in volunteer_group_permissions:
#    role, created = Group.objects.get_or_create(name=group)
#    if verbosity>1 and created:
#      print 'Creating group', group
#    for perm in myappname_group_permissions[group]: 
#      role.permissions.add(Permission.objects.get(codename=perm))
#      if verbosity>1:
#        print 'Permitting', group, 'to', perm
#    role.save()

#signals.post_syncdb.connect(
#  create_user_groups, 
#  sender=models, # only run once the models are created
#  dispatch_uid='myappname.models.create_user_groups' # This only needs to universally unique; you could also mash the keyboard
#  )