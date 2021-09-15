from .models import SocialflyUser
from django.db.models import Q
from django.db.models import CharField, Value,IntegerField
from itertools import chain
'''
USER IS RANKED BY
1)Mutual Connection (4)
2)Recommend by Socially (3)
3)Who are Following user (2)
3)Other users(1)
'''
class UserRanking:
	"""Ranking for user"""
	def __init__(self,user):
		self.user=user
		self.user_followings=self.user.following.all()
		self.query=SocialflyUser.objects.exclude(user=user)

	def mutual_connection(self):
		#the getting the mutual connection
		all_user=SocialflyUser.objects.none()
		for user in self.user_followings:
			all_user=all_user|self.assgin_ranking(user.followers.all(),'mutual connections',4)
		all_user=self.remove_unwanted_user(all_user)
		return all_user

	def socially_recomendats(self):
		#recommendation based on use is genuine
		all_user=self.remove_unwanted_user(
			self.query.filter(user__is_genuine=True)
			)

		all_user=self.assgin_ranking(all_user,'Sociafly Recommendation',3)
		return all_user.distinct()

	def user_followers(self):
		#recommendation based user followers
		all_user=self.user.followers.all()
		get_social_users=SocialflyUser.objects.none()
		for user in all_user:
			get_social_users=get_social_users|SocialflyUser.objects.filter(user=user)
		all_user=self.assgin_ranking(self.remove_unwanted_user(get_social_users),
			'Follows You',2)
		return all_user.distinct()


	def other_users(self,main_list):
		list_other_users=SocialflyUser.objects.none()
		for user in  self.query:
			if user not in main_list:
				list_other_users=list_other_users|SocialflyUser.objects.filter(user=user)
		return list(self.remove_unwanted_user(self.assgin_ranking(list_other_users,'you may know',1)))


	def arrange_the_users(self):
		mutual_connection=self.mutual_connection()
		socially_recomendats=self.socially_recomendats()
		user_followers=self.user_followers()
		all_user_list=mutual_connection.union(socially_recomendats, 
			user_followers,all=True)
		distinct_users=[]
		for user in all_user_list:
			if user not in distinct_users:
				distinct_users.append(user)
			else:
				try:
					inx=distinct_users.index(user)
					distinct_users[inx].ranking+=user.ranking
				except IndexError:
					pass
		
		distinct_users=distinct_users+self.other_users(distinct_users)
		distinct_users.sort(key=lambda user: user.ranking,reverse=True)
		return distinct_users[:12]

	def assgin_ranking(self,query_set,reason,value):
		return query_set.annotate(
				 recommend_reason=Value(reason, output_field=CharField()),
				 ranking=Value(value, output_field=IntegerField())
				)

	def remove_unwanted_user(self,query_set):
		return query_set.exclude(
			 Q(user__in=self.user_followings)
			).exclude(user=self.user)

		
	
