-- DEV (Damask Dome) -> PROD
-- change product stripe correspondance id from dev to prod
-- Use : in sqlite3 prompt : .read <filename>.sql

/* Select all massages
SELECT id, name, stripe_product_id, stripe_price_id FROM core_massage;
*/

-- "Massage personnalisé : La Parenthèse 1 heure" : id : 1
UPDATE core_massage SET 
    stripe_product_id = 'prod_UsXHWNYzV2Y6Zo',
    stripe_price_id = 'price_1U8ioHIBHqwpYiZw41L9lysU' WHERE 
        stripe_product_id = 'prod_UsXHWNYzV2Y6Zo' AND 
        stripe_price_id = 'price_1TsmCzRBrGMIS9Ri8BvlIYTK'; -- WHERE name = 'Massage personnalisé : La Parenthèse 1 heure';

-- "Massage : Le Ciblé 45 minutes" : id : 2
UPDATE core_massage SET 
    stripe_product_id = 'prod_UsWx9A8NrKoYcO',
    stripe_price_id = 'price_1U8ioeIBHqwpYiZwpTATu0KK' WHERE 
        stripe_product_id = 'prod_UsWx9A8NrKoYcO' AND 
        stripe_price_id = 'price_1TsltIRBrGMIS9Ri0Y0sDHPU'; -- WHERE name = 'Massage : Le Ciblé 45 minutes';

-- "Massage Le Ciblé 1 heure" : id : 3
UPDATE core_massage SET 
    stripe_product_id = 'prod_UsWuX6kgBbBn4h',
    stripe_price_id = 'price_1U8ionIBHqwpYiZwTdeyS8cz' WHERE 
        stripe_product_id = 'prod_UsWuX6kgBbBn4h' AND 
        stripe_price_id = 'price_1TslqgRBrGMIS9RihvRPkKnI'; -- WHERE name = 'Massage Le Ciblé 1 heure';

-- "Massage Détente : L'Étoile 30 minutes" : id : 4
UPDATE core_massage SET 
    stripe_product_id = 'prod_UsX5eQw7WxuT7O',
    stripe_price_id = 'price_1U8ip0IBHqwpYiZwQJTofhbe' WHERE 
        stripe_product_id = 'prod_UsX5eQw7WxuT7O' AND 
        stripe_price_id = 'price_1Tsm18RBrGMIS9Ri1uRdJBqR'; --WHERE name = "Massage détente : L'Étoile 30 minutes";

-- "Massage bien-être sur mesure : L'Absolu 1 h 30 minutes" id : 5
UPDATE core_massage SET 
    stripe_product_id = 'prod_UsXICUwpdZnrk4',
    stripe_price_id = 'price_1U8ipAIBHqwpYiZwfLl7BEOF' WHERE 
        stripe_product_id = 'prod_UsXICUwpdZnrk4' AND 
        stripe_price_id = 'price_1TsmE7RBrGMIS9RiK4UdCFx7'; -- WHERE name = "Massage bien-être sur mesure : L'Absolu 1 h 30 minutes";

-- "Massage du visage : Le Gua Sha 45 minutes" : id : 6
UPDATE core_massage SET 
    stripe_product_id = 'prod_UsXGjuWOuXbClr',
    stripe_price_id = 'price_1U8ipGIBHqwpYiZwEQU87ntI' WHERE 
        stripe_product_id = 'prod_UsXGjuWOuXbClr' AND 
        stripe_price_id = 'price_1TsmBtRBrGMIS9Ri5nhCxF4P'; --WHERE name = 'Massage du visage : Le Gua Sha 45 minutes';

-- "Massage Prénatal : Le Rituel 45 minutes" : id : 7
UPDATE core_massage SET 
    stripe_product_id = 'prod_UsX1FZee0ITzKw',
    stripe_price_id = 'price_1U8ipOIBHqwpYiZw8KBPyYEr' WHERE 
        stripe_product_id = 'prod_UsX1FZee0ITzKw' AND 
        stripe_price_id = 'price_1TslxgRBrGMIS9Ri6IlLFyeY'; -- WHERE name = 'Massage prénatal : Le Rituel 45 minutes';

-- "Massage Prénatal : Le Rituel 1 heure" : id : 8
UPDATE core_massage SET 
    stripe_product_id = 'prod_UsX0DXysDBEwkS',
    stripe_price_id = 'price_1U8ipWIBHqwpYiZwCl2bcY7Z' WHERE 
        stripe_product_id = 'prod_UsX0DXysDBEwkS' AND 
        stripe_price_id = 'price_1TslwHRBrGMIS9RifTdonV8L'; --  WHERE name = 'Massage prénatal : Le Rituel 1 heure';

-- "Massage Prénatal : Le Rituel 1 h 15 minutes" : id : 9
UPDATE core_massage SET 
    stripe_product_id = 'prod_UsWyesxFtT2cXc',
    stripe_price_id = 'price_1U8ipoIBHqwpYiZwepdtH9fR' WHERE 
        stripe_product_id = 'prod_UsWyesxFtT2cXc' AND 
        stripe_price_id = 'price_1TslujRBrGMIS9RiJ7NKcdC4'; -- WHERE name = 'Massage prénatal : Le Rituel 1 h 15 minutes';
        
/* Select all giftcards
SELECT id, name, stripe_product_id, stripe_price_id, stripe_coupon_id FROM core_giftcard;
*/

-- "Carte Cadeau 30min" : id : 1 
UPDATE core_giftcard SET 
    stripe_product_id = 'prod_TF39rF5ssnRX1s',
    stripe_price_id = 'price_1SIZ3CIBHqwpYiZwmBO0a0LH',
    stripe_coupon_id = 'ixMsZBos' WHERE
        stripe_product_id = 'prod_TZxbHYNgLmPDfJ' AND 
        stripe_price_id = 'price_1Scng2RBrGMIS9RiH7xjTlQp' AND
        stripe_coupon_id = 'K2Y0yTrq'; -- name = 'Carte Cadeau 30 minutes';

-- "Carte Cadeau 45min" : id : 2
UPDATE core_giftcard SET 
    stripe_product_id = 'prod_UFDPjOpA7HmBxe',
    stripe_price_id = 'price_1TGiybIBHqwpYiZwoaWCWw2Y',
    stripe_coupon_id = 'B64nljjD' WHERE
        stripe_product_id = 'prod_TZxfcJlpbuhVzR' AND 
        stripe_price_id = 'price_1ScnkaRBrGMIS9RiLlE7y8nB' AND
        stripe_coupon_id = 'meYHy1Z1'; -- name = 'Carte Cadeau 45 minutes';

-- "Carte Cadeau 1h" : id : 3 
UPDATE core_giftcard SET 
    stripe_product_id = 'prod_TF379nRt48UQ0C',
    stripe_price_id = 'price_1SIZ12IBHqwpYiZwPLqWbIS9',
    stripe_coupon_id = 'zZFx9gCU' WHERE
        stripe_product_id = 'prod_TZxhPL2yphH22W' AND 
        stripe_price_id = 'price_1ScnmVRBrGMIS9RimjAnqzAM' AND
        stripe_coupon_id = 'nMEsJAFa'; -- name = 'Carte Cadeau 1 heure';

-- "Carte cadeau 1h15" : id : 4 
UPDATE core_giftcard SET 
    stripe_product_id = 'prod_UFEEwylqvwXRmg',
    stripe_price_id = 'price_1TGjmEIBHqwpYiZwCudxthCv',
    stripe_coupon_id = '3TfYrXJR' WHERE
        stripe_product_id = 'prod_UsyGR9OUGMSVMB' AND 
        stripe_price_id = 'price_1TtCK0RBrGMIS9RiLEwRTLXj' AND
        stripe_coupon_id = 'b7EXLizY'; -- name = 'Carte Cadeau 1 h 15 min';

-- "Carte Cadeau 1h30" : id : 5 
UPDATE core_giftcard SET 
    stripe_product_id = 'prod_TF36nE9Lquh4rT',
    stripe_price_id = 'price_1SIZ0FIBHqwpYiZwOEVtAkog',
    stripe_coupon_id = 'eUWW1lYt' WHERE
        stripe_product_id = 'prod_TZxj1hRVncAKKa' AND 
        stripe_price_id = 'price_1ScnnnRBrGMIS9RikmD8eE1K' AND
        stripe_coupon_id = 'vT6Eb03G'; -- name = 'Carte Cadeau 1 h 30 min';

/* Select all Bundles
SELECT id, name, stripe_product_id, stripe_price_id FROM core_bundle;
*/

-- "Forfait 3H" : id : 1 
UPDATE core_bundle SET 
    stripe_product_id = 'prod_TF3DMfXNoVlsSi',
    stripe_price_id = 'price_1SIZ6oIBHqwpYiZwjBCOgdDQ' WHERE
        stripe_product_id = 'prod_TZxXnTKjwwawQX' AND
        stripe_price_id = 'price_1ScnccRBrGMIS9Rib2eVT9jb';-- name = 'Forfait 3 heures';

-- "Forfait 5H" : id : 2 
UPDATE core_bundle SET 
    stripe_product_id = 'prod_TF3Cvru0cFqY9e',
    stripe_price_id = 'price_1SIZ6NIBHqwpYiZwnBPvbKEK' WHERE
        stripe_product_id = 'prod_TZxY9SljD0Xel0' AND
        stripe_price_id = 'price_1ScndlRBrGMIS9RiaG8O7IKP';-- name = 'Forfait 5 heures';

-- "Forfait 10H" : id : 3 
UPDATE core_bundle SET 
    stripe_product_id = 'prod_TF3BPyqDnT33bj',
    stripe_price_id = 'price_1SIZ5KIBHqwpYiZwxNnQfDuy' WHERE
        stripe_product_id = 'prod_TZxZwY2JLVc3RP' AND
        stripe_price_id = 'price_1ScneaRBrGMIS9RiXONu9f3X';-- name = 'Forfait 10 heures';


