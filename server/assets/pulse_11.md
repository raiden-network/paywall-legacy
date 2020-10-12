---
title: Raiden Pulse #11: News from March and April
description: Overall development progress, product updates, (virtual) event participation and all the other stuff that we’ve been up to in March and April.
date: 2020-05-08
imageUrl: https://miro.medium.com/max/700/1*Ky5TKwEBt55-NlY7kBhppA.png
preview: >
  Yet another two months have passed by and it’s time for the bi-monthly summary of all things Raiden: overall development progress, product updates, event participation and all the other stuff that we’ve been up to in March and April.
  While big parts of the World, as we know it, have been on hold for the last two months, the Raiden team has continued to work towards the Alderaan release.
  We hope you’re all staying safe in these hard times and that it won’t be long before things can go back to normal. Let’s dig into what’s new with Raiden!
---


Yet another two months have passed by and it’s time for the bi-monthly summary of all things Raiden: overall development progress, product updates, event participation and all the other stuff that we’ve been up to in March and April. While big parts of the World, as we know it, have been on hold for the last two months, the Raiden team has continued to work towards the Alderaan release. We hope you’re all staying safe in these hard times and that it won’t be long before things can go back to normal. Let’s dig into what’s new with Raiden!


### Development Updates towards Alderaan mainnet

The main focus over the course of the last two months has been on extensive testing on the Alderaan release. A handful of release candidates were made and tested thoroughly on testnets and the Ethereum mainnet. There are still a couple of minor bugs that the team wants to fix before the next release candidate is released. The Raiden Wizard is also getting a refactoring and is being updated to work on the mainnet too. The goal of the Raiden Wizard is to provide users with a tool that makes it easy to get started with Raiden.

Alderaan will be the first integrated mainnet release coming with a [service layer](https://medium.com/raiden-network/raiden-service-bundle-explained-f9bd3f6f358d) (monitoring and pathfinding service) together with new features (channel withdrawal, source routing, mediation fees).


### General Updates



*   **Raiden Client:** The main focus over the last two months has been testing. The team has carried out extensive testing using the scenario player where the goal was to get at least three “all green” runs in a row, before making a new release candidate to begin testing manually. A handful of release candidates have been released since then as a result of having three green scenario runs consecutively. A significant amount of time has been spent on manually testing Raiden on the testnets and once the team was confident on the testnets, testing was moved to the Ethereum mainnet. The current goal is to run all the scenarios on the mainnet too. However, this requires some adjustments to the scenario player in order to make sure that funds can securely be recovered after a scenario has run.  \
The team is currently also fighting a couple of bugs caused by block pruning on the Ethereum mainnet clients. This problem did not show up during testing on the testnets, since they have far less transactions and events to filter for, but only showed up once mainnet testing started.

    Lastly, the Client Team has started a reiteration of the Raiden Wizard, in order to make the onboarding experience and ease of use for Raiden as seamless as possible. All releases can be found on the [Raiden client release page](https://github.com/raiden-network/raiden/releases).

*   **Raiden [light client](https://github.com/raiden-network/light-client):** The light client has seen two very productive months. Efforts have mainly been focused on implementing functionality for the light clients to be able to receive transfers, participate in mediation and to make transfers faster by using WebRTC as the transport layer. Take a look [here](https://github.com/raiden-network/light-client/releases) for a full overview of recent changes.
*   **Raiden Trust: **The Raiden Trust has [announced](https://medium.com/raiden-network/raiden-trust-updates-3e2b158aa56e) its first grantee. Congratulations to [PISA](https://www.pisa.watch/) for receiving the first Raiden Trust grant. Together with the announcement of the first grant, it was also announced that 16m RDN tokens will be moved from the Raiden Multisig to the Raiden Trust Multisig. You can, at any time, apply for a Raiden Trust grant! Find all details about grant applications and guidelines [here](https://www.raidentrust.li/). 
*   **Raiden WebUI:** The Raiden WebUI is currently undergoing a redesign with the goal of making interaction with and understanding of Raiden easy and straightforward.
*   **Weekly development updates:** u/BOR4 and u/Mat7ias have as always put in an amazing effort and continued to consistently create the weekly updates about Raiden. As always, if you are interested in more detailed development updates, please make sure to follow the weekly updates on development progress and other activities posted on [Reddit](https://www.reddit.com/r/raidennetwork/) by u/BOR4 or u/Mat7ias with the [GIT] label. 


### People


### Events



*   March 3rd-5th: We attended EthCC in Paris. On Thursday the 5th, Jacob and Kelsos did a Raiden light client workshop.
*   March 22nd: Jacob presented Raiden at ETHVR0. Follow [this link](https://twitter.com/ethereumvr/status/1241744057597976576?s=20) to see the full meetup.
*   April 4th: We presented at Noncon. Presentation available [here](https://youtu.be/0fR3uBXnIbY).


### What’s up next?



*   The entire Raiden team is working heads down to get the next mainnet release (Alderaan) out as soon as possible and we hope to be able to share some good news regarding this in the near future.
*   We are planning to participate in a bunch of hackathons as soon as Alderaan is released. 
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

