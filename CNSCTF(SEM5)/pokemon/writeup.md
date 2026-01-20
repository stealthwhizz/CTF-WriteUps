# Pokémon Ping Writeup

## Challenge Information
- **Name**: Pokémon Ping
- **Category**: Networking / Misc
- **Points**: (Not specified)
- **Description**: Professor Oak is testing his new Pokémon communication server. He claims only Pokémon Trainers with the right knowledge can reach his server and get the secret. Ash's Fighting and steel type pokemon has come forward to assist you. Can you "get" the flag with its assistance? Enter the server (0.cloud.chals.io) by following route 31986. Flag format: isfcr{}

## Solution

The challenge involves connecting to a server at `0.cloud.chals.io` on port `31986`. The hint mentions "Ash's Fighting and steel type pokemon," which refers to Lucario, a Fighting and Steel-type Pokémon from the Pokémon series.

Upon connecting to the server using tools like `telnet` or `nc`, the connection is established but immediately closed if no input is provided. This suggests the server expects user input.

Sending "Lucario" as input to the server yields the flag.

### Steps to Reproduce
1. Connect to the server:
   ```
   telnet 0.cloud.chals.io 31986
   ```
   or
   ```
   nc 0.cloud.chals.io 31986
   ```

2. Send "Lucario" as input:
   ```
   echo "Lucario" | nc 0.cloud.chals.io 31986
   ```

3. The server responds with the flag.

## Flag
isfcr{Luc4r1o_i5_th3_0G}

## Notes
- Lucario is indeed Ash's Fighting and Steel-type Pokémon in the Pokémon anime series.
- The flag confirms that Lucario is the "OG" (Original Gangster, meaning the original or classic choice).