---
title: Raiden Pulse #10: News from January and February
description: Overall development progress, product updates, (virtual) event participation and all the other stuff that we’ve been up to in January and February.
date: 2020-03-09
imageUrl: https://miro.medium.com/max/700/1*YoWpq83tOhDuqCSptoHwqA.png 
preview: >
  It is time for our bi-monthly summary of all things Raiden: overall development progress, product updates, event participation and all the other stuff that we’ve been up to in January and February.
  We hope you all had a good start to the new decade. Let’s dig into what’s new with Raiden!
---

# Raiden Pulse #10: News from January and February

It is time for our bi-monthly summary of all things Raiden: overall development progress, product updates, event participation and all the other stuff that we’ve been up to in January and February. We hope you all had a good start to the new decade. Let’s dig into what’s new with Raiden!


### Development Updates towards Alderaan mainnet

The last two months have mainly been used for fixing known bugs in the messaging transport layer. The goal of this is to get Raiden into a state where it is stable and robust enough to make it into a new release candidate and ultimately become the [Alderaan milestone](https://github.com/raiden-network/raiden/milestone/14). 

Alderaan will be the first integrated mainnet release coming with a service layer (monitoring and pathfinding service) together with new features (channel withdrawal, source routing, mediation fees).


### General Updates



*   **Raiden Client:** Fixing bugs, optimizing Matrix and improving the scenario player have been our main priorities over the last two months. The team has been working on fixing bugs, which are mostly related to Matrix, which is the protocol that we use for messaging transport. There has also been a focus on optimizing how we use Matrix as well as making Raiden more robust in the way that it utilizes Matrix.  \
Lastly, the scenario player, which is used on a nightly basis to run end to end tests of Raiden, has seen some improvements especially to the infrastructure on which it runs. With these changes, we are getting closer to announcing a new release. All releases can be found on the [Raiden client release page](https://github.com/raiden-network/raiden/releases). 
*   **Raiden [Light Client](https://github.com/raiden-network/light-client):** The light client has seen plenty of improvements and there’s been two new releases as well as two minor releases. The main focus of the releases has been UI/UX improvements. The Raiden dApp frontend now includes support for derived subkeys. This means that users don’t have to manually sign 7 messages for every transfer, which hugely improves the user experience of the dApp. Take a look [here](https://github.com/raiden-network/light-client/releases) for a full overview of recent changes.
*   **Raiden Trust: **The Raiden Trust has finished reviewing its first batch of applications and will shortly release communications about this. However, you can, at any time, apply for a Raiden Trust grant! Find all details about grant applications and guidelines [here](https://www.raidentrust.li/). 
*   **Raiden WebUI:** The Raiden WebUI continues to be fine tuned for making the UI/UX more intuitive and user friendly. We look forward to sharing this work in the near future.
*   **Weekly development updates:** u/BOR4 and u/Mat7ias have as always put in an amazing effort and continued to consistently create the weekly updates about Raiden. They reached the Weekly Update number 100, which is quite impressive and shows the dedication they are putting into their work. As always, if you are interested in more detailed development updates, make sure to follow the weekly updates on development progress and other activities posted on [Reddit](https://www.reddit.com/r/raidennetwork/) by u/BOR4 or u/Mat7ias with the [GIT] label. 


### People

Unfortunately, during the last two months we had to say goodbye to Rakan and Franzi. Both Rakan and Franzi played a vital role in the development of Raiden over the last 1.5 years. Raken contributed with very valuable work on the Raiden core and Franzi has done an amazing job working on comms and community management for the Raiden project. We are sure that wherever you go next you’ll be highly valued and we wish you both all the best in the future! &lt;3

Lefteris, who is a long standing member of the Raiden team, has started working on another new project for brainbot technologies. More news about this new project will be shared in the due course of time.

On a more positive note, we’re happy to announce that Kamal has joined the team. He will take the role as project manager for the Raiden project. We’re looking forward to working with Kamal and we’re sure that he will bring valued skills to the team. 


### Events



*   March 3rd-5th: We attended EthCC in Paris. On Thursday the 5th, Jacob and Kelsos did a Raiden light client workshop.


### What’s up next?



*   The entire team is working heads down to get the next mainnet release (Alderaan) out as soon as possible and we hope to be able to share some good news regarding this in the near future.
*   We are going to sponsor and talk at NonCon, which is the replacement event for Edcon this year. We hope to soon be able to announce Raiden participation at some hackathons as well.
*   Please make sure to follow our [Twitter feed](https://twitter.com/raiden_network) for more announcements on upcoming events. 


### Join our team!

Looking for a new challenge? If you want to be part of an open ecosystem right at the technological frontier and happen to be as excited about payment channel networks as we are, please have a look at the [open positions](https://angel.co/brainbot-group/jobs) and apply or feel free to refer somebody.

All the best,

The Raiden Team

- - - 

Make sure to stay up to date by following us on [Twitter](https://twitter.com/raiden_network) and [Medium](https://medium.com/raiden-network) and joining the conversations on [Reddit](https://www.reddit.com/r/raidennetwork/) and [Gitter](https://gitter.im/raiden-network/raiden)!

_The Raiden project is led by brainbot labs Est._

- - - 

Disclaimer: Please note, that even though we do our best to ensure the quality and accuracy of the information provided, this publication may contain views and opinions, errors and omissions for which the content creator(s) and any represented organization cannot be held liable.

The wording and concepts regarding financial terminology (e.g. “payments”, “checks”, “currency”, “transfer” [of value]) are exclusively used in an exemplary way to describe technological principles and do not necessarily conform to the real world or legal equivalents of these terms and concepts.

