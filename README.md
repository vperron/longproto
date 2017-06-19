# longproto

Long-polling prototype

## Simulate disconnections
The easiest way to simulate disconnections is to use a different server, and
cut the cable.

With the current (quite aggressive) settings, the half-open connection is closed
after 3 seconds, immediately, and the client starts polling.

## Data consumption
A proposed modus operandi (to be tested in the field) could be the following:

- Keep the connection open in long-polling mode for as long as necessary.
  Have a timeout to close the connection without data exchange after 4 minutes.

- Send keepalives every 15 seconds, as is the "acceptable" time for a human
  to wait for an unlock / action to proceed. With Bluelink it's 20.

- If the keepalive does signal a dropped connection, immediately stop it and
  try opening a new one.

This leads to:

1. One packet (3-way handshake) for the connexion establishment, that eventually timeouts.
2. No TLS: what's the need on this channel? We'll receive unidirectional commands.
   What's the use to an attacker?
3. One packet is sent back with the command payload, if needed, but it's useful data.
4. Keepalives are sent every 15 seconds, those are zero-data packets with a very high
   chance of not being counted as "data".
5. After the first failed keepalive, we reconnect.

Which leads us to:

74+74+66+211+66 = 384
---------------------
425 bytes for the connection establishment, maybe not counted. X by hour without command.
We can drop the headers for more economy (Accept-Encoding, Host...)

4608 bytes/hour if the handshakes count.
2832 bytes/hour if they don't.

66 * 2 bytes for the keepalives.
31680 bytes per hour if the keepalives count.
0 bytes per hour if they don't.

0 bytes for the connection drop after the timeout.

The command payloads are considered useful and uncompressible data.

So that goes...

WORST CASE: 26Mb / month.
NO TCP HANDSHAKES: 24MB / month.
TCP HANDSHAKES, NO KEEPALIVES: 3MB / month.
ONLY HTTP HELLO: 1.9MB / month.

That's just the "overhead" traffic, the actual payloads will take some data cap.


## Canal reuse
We can leverage Asyncio to reuse the same channel for telemetry data. Lowers the
first handshake cost.
A direct sample that I did not code properly yet:
https://stackoverflow.com/questions/22190403/how-could-i-use-requests-in-asyncio


## Next steps
Buy a SIM and check if the Keepalives and such are counted in the data.
Reduce the actual payload sizes.
Tune the numbers.



# Other Solutions

## SMS
Le SMS est un moyen de notification PUSH builtin dans le protocole GSM.
L'utilisation "texte" est un hack; c'est là pour des notifications !
Utiliser le SMS binaire pour les appairages et les commandes VE semble une bonne idée.
Plus besoin de long polling, websockets, etc.
Le prix est à discuter mais chaque opération PUSH est en théorie "rentable" (prise de location,
etc) donc ce n'est pas si important.

Auquel cas, on peut se limiter à des HTTP POST tout bêtes pour la télémétrie.

## SSL
Autant le SMS (ou toute communication server -> client) peut etre non sécurisé, sans impact;
autant l'envoi de télémétrie dans le DC est plus sensible. Le SSL est donc recommandé,
mais il faut faire attention au Key Exchange dans lequel une latence de ~200ms est à
prévoir, et surtout un échange de certificats a lieu.

Heureusement, SSL (puis TLS) supportent un mécanisme pour ne plus télécharger le CRT a chaque
fois, il s'agit de la Session Resumption (avec Session Cache ou Client Tickets)
https://hpbn.co/transport-layer-security-tls/#tls-session-resumption

Ceci s'active assez facilement dans Nginx.
http://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_session_tickets

Cela permet de n'effectuer qu'un seul échange de clés par heure, par exemple.


## Sigfox / LoRa
Au prix d'une intégration plus couteuse et la nécessité de gateways, on peut aussi explorer
ces pistes.
