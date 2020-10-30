# memesgarden
## CWF2020 Fall and IT2002 Project

### Project built using Django with PostgreSQL for a database. Mock data created using Mockaroo.


### Backstory:
Welcome to MemesGardens, a futuristic community garden where individuals can grow and harvest very interesting stuff like plants!
These plants can be either eaten or be used for decorations... But occasionally it can be used for some very interesting interactions.
Food security is very important in these times, and clearly, community gardens and vertical farming are potential ways to further secure food supply.
As you might have noticed, the notifications in these messages can look a little more communal. Hm. Interesting. Why stop at food security?
We should learn to have fun in these troubling times! Food makes us a little less hangry, memes make us happy. If MemesGarden cannot save the world and make us happy at the same time,
I don't know what will! Just imagine injecting all the life and memes into the plants in MemesGarden and you're still sad and the world ends!
We be happy, we be healthy, we be saved and we be fine! What more can we ask for!

### There are a few components here:
1) Users(*user_id*, *email*, first_name, last_name, gender, contact_number, password, points)
2) Pots(*pot_id*, location, pot_length, pot_width, pot_height, plant, plant_type)
3) Ownership(*pot_id*, user_id, is_registered, date_of_registration)
4) Rewards(*reward_id*, reward, img, points_required, valid_till)
5) Redemption(*redemption_id*, reward_id, user_id, redeem_datetime, has_been_used)
6) Tasks(*task_id*, task, target_pot, requester_id, assignee_id, points_given, datetime_opened, is_done, urgency)

### Relationships:
* A user can own many pots.
* One pot can be owned only by one user, where a pot can own a plant that is used either for DECO or FOOD.
* A user can take up to 10 tasks, and a user can request a maximum of 10 tasks.
* A user can redeem as many rewards as he or she wants, as long as he or she has sufficient points.
* A user can have no limits to redemption of rewards, but its usability varies based on the validity date (I GOT A -YEET~).
* Tasks that are complete are irrelevant.
* Rewards that have been redeeemed are irrelevant.
* Rewards whose validity date have been passed can still be redeemed but not used (the same rewards can be re-released in future, YOU BETTER PRAY M8).

P.S. Since this project is part of a school project, I got no demo and it is complete. However, you may access the project by using:
* Username: kcard3@sciencedaily.com
* Password: v5LL4X264CF
