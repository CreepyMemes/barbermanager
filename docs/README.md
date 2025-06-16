<div align="center"><img src="./Implementazione/frontend/public/logo.png" height="100px" alt="BarberManager Logo"/></div>

<h1 align="center">BarberManager – Un software gestionale per barber shop</h1>

# Descrizione

BarberManager è una piattaforma pensata per digitalizzare e semplificare la gestione delle attività di un barber shop, focalizzandosi su:

- Gestione **account**
- Registrazione **clienti e barbieri**
- Prenotazione **appuntamenti**
- Gestione del **personale**
- Area **amministrativa**

## Gestione Account

Gli account si dividono in tre ruoli principali:

- **Admin**: può essere creato **solo tramite shell**
- **Clienti**: possono registrarsi tramite la **piattaforma web**
- **Barbieri**: possono registrarsi **solo se invitati da un admin** tramite email

Tutti gli utenti possono:

- Accedere tramite credenziali
- Recuperare la password via email, cliccando sul link e inserendone una nuova
- Modificare o eliminare il proprio account

## Registrazione

La registrazione varia a seconda del ruolo dell'utente:

- **Admin**: vengono creati **manualmente tramite shell**, inserendo:

  - Username unico
  - Password

- **Clienti**: possono registrarsi autonomamente tramite l'applicazione. Per completare la registrazione, è necessario **verificare l’indirizzo email** cliccando sul link ricevuto via email. Durante la registrazione devono fornire:

  - Dati personali
  - Email valida
  - Username unico
  - Password

- **Barbieri**: possono registrarsi **solo tramite invito da parte di un admin**. Ricevono un'email con un link d’invito e, cliccandolo, completano la registrazione inserendo:
  - Dati personali
  - Username unico
  - Password

## Prenotazione Appuntamenti

I clienti possono avere **una sola prenotazione attiva per volta**. Il processo di prenotazione segue questi passaggi:

1. Visualizzazione della lista dei **barbieri disponibili**
2. Scelta del **barbiere preferito**
3. Visualizzazione dei **servizi offerti** dal barbiere selezionato
4. Selezione dell'orario desiderato tra le **disponibilità orarie** del barbiere
5. Conferma della prenotazione

Il sistema:

- Salva automaticamente la prenotazione
- Invia **promemoria via email** prima dell’orario dell’appuntamento
- Mostra lo storico delle prenotazioni nel profilo del cliente

## Gestione Prenotazioni

I clienti possono:

- **Annullare** una prenotazione, se **non ancora completata**
- Lasciare una recensione **solo al barbiere con cui hanno avuto un appuntamento**, e **una sola volta per ciascun barbiere**
- Consultare la lista dei propri **appuntamenti precedenti**

## Gestione del Personale

I **barbieri**, tramite la loro area riservata, possono:

- Visualizzare gli **appuntamenti assegnati**
- Aggiungere, modificare o eliminare i **servizi che offrono**
- Visualizzare le proprie **recensioni ricevute** dai clienti

## Area Amministrativa

Gli **admin**, tramite pannello dedicato, possono:

- **Aggiungere o rimuovere barbieri**
- Gestire le **disponibilità dei barbieri**
- Visualizzare **statistiche dettagliate** sulle attività del salone
