# Green Groove

**Green Groove** is a student-built RFID + sensor retail system designed to remove manual basket reconstruction from checkout. It connects shopper identity, shelf events, a live virtual cart, reversible returns, and final billing into one physical-digital flow.

The project was **selected under NCERT PRAYAAS (Promotion of Research Attitude among Young And Aspiring Students)** in the urban private category and received a **₹50,000 development grant**. **IIT Delhi is the associated Higher Education Institution (HEI)** for our PRAYAAS project, with **Prof. Satish Kumar Dubey of SeNSE, IIT Delhi** serving as mentor through the programme. The next development phase is intended to use IIT Delhi technical facilities, institutional resources, and mentorship to strengthen and validate the prototype further.

## The question that changed the project

Green Groove began with a simple problem: supermarket queues. That led to a harder question: **why reconstruct a shopper's basket only when they reach the register?**

If identity, shelf events, and cart state can remain synchronized throughout the shopping trip, checkout can become confirmation of an already-known transaction rather than a fresh reconstruction of everything the shopper picked up.

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

## What became hard to solve

Building Green Groove exposed several problems that were more important than simply detecting that an item moved:

- **Detection is not association.** A shelf event still has to be matched to the correct shopper before state changes.
- **Physical actions must be reversible.** Returns and mistakes require explicit inverse transitions rather than silent corrections.
- **Sensors need a second opinion.** Shelf state and cart state can cross-check one another for missed, duplicate, or ambiguous events.
- **Identity has to precede automation.** A correct detection without a reliable shopper/cart context cannot safely modify transaction state.
- **Uncertainty should remain visible.** Ambiguous associations should be surfaced instead of silently forced into the wrong cart.
- **Checkout was downstream of the real problem.** Maintaining trustworthy transaction state throughout the trip turns final billing into settlement rather than reconstruction.

## External validation and next phase

Green Groove was selected under **NCERT PRAYAAS**, awarded **₹50,000** in development support, and paired with **IIT Delhi as the associated HEI**. Through the programme, **Prof. Satish Kumar Dubey (SeNSE, IIT Delhi)** is mentoring the project.

The next phase is focused on two forms of evidence:

1. **Technical validation** using further prototyping, testing, and institutional facilities/resources available through the programme.
2. **Field validation** with retail stores, including documented pilot conditions, usage evidence, observed failure modes, and store feedback rather than marketing-only testimonials.

Green Groove was created by **Sushanth Dasari and Aryan Kumar**.

## Website

This repository contains the static project site used to document the system, prototype, design decisions, evidence, and build process.

The production workflow automatically checks routes, controls, media integrity, keyboard behavior, responsive interaction, and browser regressions across Chromium, Firefox, and WebKit before publishing generated changes.

## Public references

- NCERT PRAYAAS: https://www.ncert.nic.in/desm/prayaas.php?ln=en
- Prof. Satish Kumar Dubey, SeNSE, IIT Delhi: https://sense.iitd.ac.in/faculty-profile/7
- Green Groove Behance case study: https://www.behance.net/gallery/211169339/Green-Groove
- Published school coverage: https://theglobaltimes.in/archives/december-15-2025.pdf

## GitHub Pages

Publishing source: `main` / `/ (root)`.
