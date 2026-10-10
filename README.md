# Green Groove

**Green Groove** is a student-built RFID + sensor retail system designed to remove manual basket reconstruction from checkout. It connects shopper identity, shelf events, a live virtual cart, reversible returns, and final billing into one physical-digital flow.

The project was **selected under NCERT PRAYAAS (Promotion of Research Attitude among Young And Aspiring Students)** in the urban private category and received a **₹50,000 development grant**.

## Why we built it

Green Groove began with a simple problem: supermarket queues. That led to a harder question — instead of only making queues move faster, could the transaction state be built while the shopping trip is happening so checkout becomes settlement rather than reconstruction?

That question changed the project from queue intelligence into a checkout-system prototype.

## How the prototype works

1. A shopper receives a unique RFID wristband that establishes identity and cart context.
2. Shelf load cells and RFID readers detect when a product is picked up or returned.
3. Each shelf event is associated with the relevant shopper before cart state changes.
4. The live cart updates throughout the trip, while returns reverse earlier state rather than hiding it.
5. The final invoice is generated from the cart state already built during shopping.

## What we built

The prototype is organized around three visible project modules:

- **Groove Band** — RFID shopper identity
- **Green Grooves** — sensor-assisted shelf events
- **G/G App** — live digital cart and transaction state

The website expands these into a six-layer system model: **Identity → Shelf Events → Association → Reversibility → Live Cart → Settlement**.

Green Groove was created by **Sushanth Dasari and Aryan Kumar**.

## Website

This repository contains the static project site used to document the system, prototype, design decisions, evidence, and build process.

The production workflow automatically checks routes, controls, media integrity, keyboard behavior, responsive interaction, and browser regressions across Chromium, Firefox, and WebKit before publishing generated changes.

## Public references

- NCERT PRAYAAS: https://www.ncert.nic.in/desm/prayaas.php?ln=en
- Green Groove Behance case study: https://www.behance.net/gallery/211169339/Green-Groove
- Published school coverage: https://theglobaltimes.in/archives/december-15-2025.pdf

## GitHub Pages

Publishing source: `main` / `/ (root)`.
