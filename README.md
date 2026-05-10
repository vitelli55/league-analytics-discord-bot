# A Discord bot for League of Legends Analytics.
The current main function of this bot is to retrieve the "best build" for a champion through user query in Discord -> l!build (champion name)

The idea came from the frustration of constantly alt-tabbing out of games to search for champion builds online whenever I was playing a champion I was unfamiliar with. Instead of interrupting gameplay, searching online, and waiting for occasional "alt-tab freeze", players can instantly query builds directly through the Discord overlay without minimising the game. 

## The Plan
For now: 
- From Riot's API, gather PUUID (Player Universally Unique Identifier) of players in the top ranks (challenger, grandmaster, and masters).
- From the PUUIDs, we can extract the 20 most recent match ids for each player. Duplicate matches are handled to avoid unnecessary API calls. 
- The individual match data, containing information such as items, champions, and results, is then fetched from the match id and stored locally to also avoid unnecessary API calls.
- (WHERE I'M CURRENTLY AT) The extracted information is then used to calculate item build frequency, win rates, and most common build paths. 
- The "most optimal" build for each champion is then stored. 
- When a user requests a build, the bot searches the processed dataset and returns the most relevant results instantly. Because the processing happens beforehand, response times remain fast during gameplay.

### Long-term Ideas
- Machine learning to predict best builds based on matchup.