from re import L
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Leader
from .utils import LEADER_TYPES , LEADER_TYPES_PRICES

def get_bonus_to(leader):
    if not leader.parent :
        print('no parent bonus')
        return None
    else:
        if leader.parent_relation_numbre == 1 or leader.parent_relation_numbre == 3:
            print('parent bonus')
            return leader.parent
        else:
            print('recursive get bonus')
            return get_bonus_to(leader.parent)
    # if leader.parent_relation_numbre == None :
    #     print('no parent bonus')
    #     return None
    # if leader.parent_relation_numbre == 1 or leader.parent_relation_numbre == 3 :
    #     print('parent bonus')
    #     return leader.parent    
    # print('recursive get bonus')
    # get_bonus_to(leader.parent)    

def credit_bonus(leader):
    bonus_to = get_bonus_to(leader)
    print('bonus tooo',bonus_to)
    if bonus_to == None:
        print('credited bonus to company')
        leader.bonus_type = 'company'
        leader.bonus_amount = LEADER_TYPES_PRICES[leader.leader_type]['points']
        leader.bonus_to = None
        leader.save()
    else:
        leader.bonus_type = 'parent'
        leader.bonus_amount = LEADER_TYPES_PRICES[leader.leader_type]['points']
        leader.bonus_to = bonus_to
        leader.save()
        bonus_to.points += LEADER_TYPES_PRICES[leader.leader_type]['points']
        bonus_to.save()
    


@receiver(post_save, sender=Leader)
def leader_created(sender, instance, created, **kwargs):
    print(f'signal recieved ---->')
    if created:
        print(f'Created New Leader --> [{instance}]')
        parent = instance.parent
        if parent:
            print('the parent is -->', parent)
            instance.parent_relation_numbre = parent.get_next_relation
            instance.save()
            parent.children_count += 1
            parent.save()
            credit_bonus(instance)
            # print(get_bonus_to(instance))
        else:
            print('no parent :(  ')    
    else:
        print('just an update to the parent <--')
   

# post_save.connect(leader_created, sender=Leader, )
