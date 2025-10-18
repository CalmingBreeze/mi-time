-- Restore product stripe correspondance id to prod mode
-- Use : in sqlite3 prompt : .read <filename>.sql

/* Select all giftcards
SELECT id, name, stripe_product_id, stripe_price_id, stripe_coupon_id FROM core_giftcard;
*/

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_T1DippNT0JjXtp',
    stripe_price_id = 'price_1S5BGhDFgcrRu1lO3vDIFifl',
    stripe_coupon_id = 'cOELndEv' WHERE name = 'Carte Cadeau 1h30';

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_T1DibPWV9094pF',
    stripe_price_id = 'price_1S5BGkDFgcrRu1lOmpIxflFo',
    stripe_coupon_id = 'EyEMvx2G' WHERE name = 'Carte Cadeau 1h';

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_T1Di6hClHmZnir',
    stripe_price_id = 'price_1S5BGfDFgcrRu1lOpUhwA6i0',
    stripe_coupon_id = 'k7UbKZZb' WHERE name = 'Carte Cadeau 45min';

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_T1DhTJuvbXIxo4',
    stripe_price_id = 'price_1S5BGfDFgcrRu1lOpUhwA6i0',
    stripe_coupon_id = 'LqzERQx3' WHERE name = 'Carte Cadeau 30min';

/* Select all Bundles
SELECT id, name, stripe_product_id, stripe_price_id FROM core_bundle;
*/

UPDATE core_bundle SET 
    stripe_product_id = 'prod_TF1rLpPHDftiWe',
    stripe_price_id = 'price_1SIXnQDFgcrRu1lOvkjb5pkR' WHERE name = 'Forfait 10H';

UPDATE core_bundle SET 
    stripe_product_id = 'prod_TF1qleOU7bqeDB',
    stripe_price_id = 'price_1SIXn3DFgcrRu1lO0owoNWiE' WHERE name = 'Forfait 5H';

UPDATE core_bundle SET 
    stripe_product_id = 'prod_TF1pEi3BTVEq4t',
    stripe_price_id = 'price_1SIXmBDFgcrRu1lOwnZxBzxB' WHERE name = 'Forfait 3H';
