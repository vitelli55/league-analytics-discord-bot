# A Discord bot for League of Legends analytics.

The current main function of this bot is to retrieve the "best build" for a champion through user query in Discord -> l!build (champion name)

## THE PLAN
For now: Get Riot API -> process it to filter out everything -> calculate best build -> store data in a locally or in a database -> when the user queries, it retrieves from the storage
Long-term future: machine learning to predict best builds based on matchup.