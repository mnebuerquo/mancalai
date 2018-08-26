# Running in Docker

See the [deploy](./deploy) directory for the build scripts.

# Development Interface

1. Build - You have to build the docker container before you can run it.
   ```bash
   ./deploy/build.sh dev
   ```
   This builds the docker image for _dev_ so you can run it.

   To build the api container:
   ```bash
   ./deploy/build.sh api
   ```

2. Testing - Run automated tests, then stop.

   ```bash
   ./deploy/dev.sh --ci /dev/null
   ```

3. Test Drive - Try playing the game to see if it is working correctly.
   ```bash
   ./deploy/dev.sh mancala/play.py luck
   ```
   This command will put you head to head with a very stupid AI.

4. Train - You want to train two AI players by having them play against each
   other.
   ```bash
   ./deploy/dev.sh mancala/adversary.py nn1h128 nn3h80
   ```
   This will start two different AI models playing against each other and
   training based on their wins and losses.

5. API - You want to run the api so you can play by HTTP.
   ```bash
   ./deploy/dev.sh --api
   ```
   This starts up the flask api on port 5000.
