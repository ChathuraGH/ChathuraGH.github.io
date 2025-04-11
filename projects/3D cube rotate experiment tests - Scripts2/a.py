# works
# there is a paper written by me

import random


pool=[1,2,3,4,5,6]

s_2_near=[1,5,3,6]
s_4_near=[1,5,3,6]

s_1_near=[2,5,4,6]
s_3_near=[2,4,5,6]

s_5_near=[1,4,3,2]
s_6_near=[1,2,3,4]



def Random_Box_Sequence_Generator_V1(start=1):
	sq=[start]
	for i in range(0,5):

		llist=eval(f's_{sq[-1]}_near[{random.choice([0,1,2])}]')

		# random.choice()
		print(llist)
		sq.append(llist)

	print(random.choice(pool),'zz',sq[-1],s_2_near[1],sq)


def Random_Box_Sequence_Generator_V2(start=1):
	sq=[start]
	try:
		for i in range(0,5):
			item=random.choice(list(set(eval(f's_{sq[-1]}_near'))-set(sq)))
			# random.choice()
			print(item)
			sq.append(item)
		# if(len(sq)<6):
		# 	Random_Box_Sequence_Generator_V2()
		# else:
		print(random.choice(pool),'zz',sq[-1],s_2_near[1],sq)
	except:	
		if(len(sq)<6):
			Random_Box_Sequence_Generator_V2()
		else:
			print(random.choice(pool),'zz',sq[-1],s_2_near[1],sq)





# Random_Box_Sequence_Generator_V1(1)

Random_Box_Sequence_Generator_V2(1)


