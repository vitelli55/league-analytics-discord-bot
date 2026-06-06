# A Discord bot for League of Legends Analytics.
The current main function of this bot is to retrieve the "best build" for a champion through user query in Discord -> l!build (champion name)

The idea came from the frustration of constantly alt-tabbing out of games to search for champion builds online whenever I was playing a champion I was unfamiliar with. Instead of interrupting gameplay, searching online, and waiting for occasional "alt-tab freeze", players can instantly query builds directly through the Discord overlay without minimising the game. 

## The Plan
For now: 
- From Riot's API, gather PUUID (Player Universally Unique Identifier) of players in the top ranks (challenger, grandmaster, and masters).
- From the PUUIDs, we can extract the 20 most recent match ids for each player. Duplicate matches are handled to avoid unnecessary API calls. 
- The individual json match data, containing information such as items, champions, and results, is then fetched from the match id and stored locally to also avoid unnecessary API calls.
- After collecting raw matches (about 72k matches for the first working version), for each champion, I extracted match appearances, total wins, and each item that was bought. And for each item that was bought, I also kept a count of how many times it was purchased and how many games were won with that item. This produced the file *data/processed/champion_item_stats.json*.
- I then used the gathered item stats to calculate *Pick rate*, *Win Rate*, and *WPA (Win Probability Added)*
- When a user requests a build, the bot searches the processed dataset and returns the most relevant results instantly. Because the processing happens beforehand, response times remain fast during gameplay.

# Issues I encountered
## **No Starting items** 
This is due to the difference between Riot’s standard match data and timeline data. The regular match endpoint only provides the final item build, while starting items are only reliably available through the match timeline endpoint, which tracks item purchases over time.

The reason why I don't use timeline data (yet) is because of the difference in stored size of endpoint vs timeline:
- Each match json (endpoint) is about 80kb. For the 72,000 matches I fetched, I ended up with a total of 5.54GB. 
- In the other hand, a match data file containing timelines is about 800kb.

### Long-term Ideas
- Machine learning to predict best builds based on matchup.
- Include starting items (will have to get match timelines)