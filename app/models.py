
from django.db import models
from users.models import NewUser
from django.core.validators import MinValueValidator, MaxValueValidator
from .utils import LEADER_TYPES, LEADER_TYPES_PRICES , BONUS_TYPES
from shortuuidfield import ShortUUIDField
# Create your models here.
class Leader(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    leader_type = models.CharField(choices=LEADER_TYPES,max_length=10)
    main_account = models.ForeignKey(NewUser, related_name='leaders', on_delete=models.RESTRICT)
    parent = models.ForeignKey('self',related_name= 'children' ,on_delete=models.RESTRICT, null=True , blank=True)
    parent_relation_numbre = models.PositiveIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(4)],null=True,blank=True)
    children_count = models.PositiveIntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(4)],default=0)

    
    points = models.PositiveIntegerField(default=0) 
    earnings = models.PositiveIntegerField(default=0)

    uuid = ShortUUIDField(db_index=True, max_length=8 )

    bonus_amount = models.PositiveIntegerField(null=True,blank=True)
    bonus_type = models.CharField(choices=BONUS_TYPES, max_length=10, null=True,blank=True)
    bonus_to = models.ForeignKey(
        'self', related_name='bonus_from', on_delete=models.RESTRICT, null=True, blank=True)


    def __str__(self) -> str:
        return f'{self.main_account.user_name} Leader Type [{self.leader_type.upper()}][{self.id}]'

    @property
    def is_eligible(self):
        if self.children_count < 4 and self.children_count >= 0 :
            return True
        else:
            return False    

    @property
    def is_same_type(self):
        if self.parent and self.parent.leader_type == self.leader_type:
            return True
        else:
            return False    

    @property
    def get_next_relation(self):
        if self.is_eligible :
            return self.children_count +1
        else:
            return 0

    # Overriding save method for some validation
    def save(self, *args, **kwargs):
        print('save method of [MODEL]')
        print('-----------------------')
        # if self.parent and not self.parent.is_eligible:
        #     raise ValueError(
        #         "Parent is not eligible - (Maximum children 4)")
        
        if self.parent and not self.is_same_type:
            raise ValueError(
                f"Parent [{self.parent.leader_type.upper()}] is not same type [{self.leader_type.upper()}]")
        super().save(*args, **kwargs)
