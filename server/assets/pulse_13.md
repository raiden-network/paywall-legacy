---
title: Raiden Pulse #13: News from July and August
description: Two more months have passed by and it’s time for a new bi-monthly summary of all things Raiden.
date: 2020-09-03
imageUrl: https://miro.medium.com/max/700/1*UBQGJ9Z1Z8Ib25AqNx7LEQ.png
preview: >
  Two more months have passed by and it’s time for a new bi-monthly summary of all things Raiden: overall development progress, product updates, (virtual) event participation and all the other stuff that we’ve been up to in July and August.
  The overarching focus of July was our participation in the Great Reddit Scaling Bake-Off.
  In August, the main focus has been on some maintenance work and continuing the implementation of WebRTC for the transport layer in the Raiden python client.
  The light client team is still working towards reaching parity with the Alderaan release.
  Let’s dig in!
---

Two more months have passed by and it’s time for a new bi-monthly summary of all things Raiden: overall development progress, product updates, (virtual) event participation and all the other stuff that we’ve been up to in July and August. The overarching focus of July was our participation in the Great Reddit Scaling Bake-Off. In August, the main focus has been on some maintenance work and continuing the implementation of WebRTC for the transport layer in the Raiden python client. The light client team is still working towards reaching parity with the Alderaan release. Let’s dig in!


### General Updates

-   **Raiden [Client](https://github.com/raiden-network/raiden):** In July we put a lot of time and effort into [the Great Reddit Scaling Bake-Off](https://www.reddit.com/r/ethereum/comments/hbjx25/the_great_reddit_scaling_bakeoff/). An in-depth explanation of our solution can be found in [this blogpost](https://medium.com/@raiden_network/raiddit-scaling-reddit-community-points-with-raiden-9fe60c14ae47). The solution we made is called Raiddit. In essence, Raiddit is a modified version of Raiden that utilizes virtual channels to avoid any on-chain transactions before channel settlement. This means that minting and burning also happens off-chain. Due to the design of Raiden itself, Raiddit scales linearly which means that fulfilling the scaling requirements of the Reddit challenge was not a problem at all.

    After the Reddit challenge our main focus has been on doing some general maintenance of the code base. We also continued to work on implementing WebRTC for the transport layer to get faster transfers.

-   **Raiden [Light Client](https://github.com/raiden-network/light-client):** We have also seen great progress with the Raiden light client during the last two months. It is now possible to withdraw tokens from open channels without closing the channel that you withdraw from. 

    Another great breakthrough was to have all the scenarios used by the Python client pass with the light client. The scenarios act as integration tests that mimic real life Raiden nodes that interact with each other. This is a great step towards an Alderaan compatible release of the light client. Lastly, the light client now also exposes the same API as the Python client. This is very convenient for developers building on top of Raiden, since they don’t have to worry about which Raiden client is used.

-   **Raiden [Trust](https://www.raidentrust.li/):** The Raiden Trust is currently reviewing a new round of applications. We look forward to hopefully sharing some interesting new grantees in the near future. If you’re interested in learning more about the Raiden Trust and how to apply for a grant, you can read more [here](https://www.raidentrust.li/guidelines.html).
-   **Weekly development updates:** u/BOR4 and u/Mat7ias have, as usual, put in an amazing effort and continued to consistently create the weekly updates about Raiden. If you are interested in more detailed development updates, please make sure to follow the weekly updates on development progress and other activities posted on [Reddit](https://www.reddit.com/r/raidennetwork/) by u/BOR4 or u/Mat7ias with the [GIT] label. 


### People

In July Kelsos left the project. We want to give a big thanks to Kelsos for his many contributions and his very kind and helpful personality. It was a pleasure to work with you and we wish you all the best in the future.

We’re happy to welcome Max back to the team. Max used to work with us a couple of years ago as a student. He has now finished his studies and has joined the Raiden team full time.


### Events
-   We participated in the Great Reddit Scaling Bake-Off as already described earlier in this post


### What’s up next?



-   We are currently planning the events and hackathons that we want to participate in for the next couple of months
-   Please make sure to follow our [Twitter feed](https://twitter.com/raiden_network) for more announcements on upcoming events


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
