# Avondvierdaagse Hoevelaken website

Voor de organisatie van de Avondvierdaagse Hoevelaken is deze website ontwikkeld. De website heeft als doel om mensen over de Avondvierdaagse Hoevelaken te informeren en foto's te laten zien die gemaakt zijn tijdens de Avondvierdaagse Hoevelaken.

## Design filosofie
De Avondvierdaagse Hoevelaken is een lokaal evenement dat 1 keer per jaar plaats vind. Hierdoor zal vooral vlak voor en tijdens de Avondvierdaagse Hoevelaken de website bezocht worden. De website heeft dus niet veel verkeer te verwerken.

Voor de beheerkant moet niet verwacht worden dat iedereen die informatie wil zetten, ook technisch aangelegd is. Voor het beheer gedeelte is het daarom belangrijk dat alles intuïtief is en er sprake is van WYSIWYG.

Met deze informatie in het achterhoofd zijn keuzes voor het ontwerp van de website gemaakt. Zo is gebruik gemaakt van EditorJS ([github](https://github.com/codex-team/editor.js/tree/next)  / [website](https://editorjs.io/)) voor het bewerken van de tekst op pagina's.

## Deployment

Deployment kan nu gedaan worden door de 'release'-branch te clonen op de server. Naast de `docker-compose.yml` kan dan een `.env` met settings gemaakt worden. Door de docker-compose te draaien zal de applicatie beschikbaar zijn.

De applicatie doet niets met het controleren van de hostname of ssl certificaten. Er wordt aangenomen dat op de host een Nginx/Apache draait die dit regelt.

Dit is een voorbeeld van een Nginx configuratie:

```config
server {
	listen [::]:443;
	listen 443 ssl;
	ssl_certificate <ssl_certificate_bundle>;
	ssl_certificate_key <certificate_key>;
	ssl_prefer_server_ciphers on;

	resolver 127.0.0.1;
	ssl_stapling on;
	ssl_stapling_verify on;
	ssl_trusted_certificate <ssl_certificate_bundle>;

	server_name <hostname>.nl www.<hostname>.nl;

	location / {
		proxy_pass http://localhost:1337;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_redirect off;
	}
}


server {
	listen 80;
	listen [::]:80;

	server_name <hostname>.nl www.<hostname>.nl;

	return 301 https://$host$request_uri;
}

```


## Settings

Settings zijn niet verplicht toe te voegen. In de code zitten fallbacks om het weglaten van variabelen op te vangen als deze niet aanwezig zijn.

| Env variabelen      | Beschrijving                                                                              |
| ------------------- | ----------------------------------------------------------------------------------------- |
| SECRET_KEY          | Django SECRET_KEY value                                                                   |
| DEBUG               | 0 voor productie, 1 voor development                                                      |
| DB_ENGINE           | Welke engine van django gepakt moet worden (django.db.backends.) (bijv. mysql of sqlite3) |
| DB_HOST             | Database HOST setting                                                                     |
| DB_PORT             | Database PORT setting                                                                     |
| DB_NAME             | Database NAME setting                                                                     |
| DB_USER             | Database USER setting                                                                     |
| DB_PASS             | Database PASSWORD setting                                                                 |
| DB_ROOT_PASS        | Database root password (voor bijv. mysql)                                                 |
| DB_CHARSET          | Database OPTIONS.charset setting                                                          |
| SESSION_COOKIE_NAME | Django session cookie name                                                                |
| EXTERNAL_PORT       | Poort van de host-server waarop de applicatie beschikbaar is                              |
