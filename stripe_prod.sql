-- Restore product stripe correspondance id to prod mode
-- Use : in sqlite3 prompt : .read <filename>.sql

/* Select all giftcards
SELECT id, name, stripe_product_id, stripe_price_id, stripe_coupon_id FROM core_giftcard;
*/

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_TF36nE9Lquh4rT',
    stripe_price_id = 'price_1SIZ0FIBHqwpYiZwOEVtAkog',
    stripe_coupon_id = 'eUWW1lYt' WHERE name = 'Carte Cadeau 1h30';

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_TF379nRt48UQ0C',
    stripe_price_id = 'price_1SIZ12IBHqwpYiZwPLqWbIS9',
    stripe_coupon_id = 'zZFx9gCU' WHERE name = 'Carte Cadeau 1h';

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_TF38FMQN0nFoaB',
    stripe_price_id = 'price_1SIZ2IIBHqwpYiZweXsWptgt',
    stripe_coupon_id = 'xyK9FjbR' WHERE name = 'Carte Cadeau 45min';

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_TF39rF5ssnRX1s',
    stripe_price_id = 'price_1SIZ3CIBHqwpYiZwmBO0a0LH',
    stripe_coupon_id = 'ixMsZBos' WHERE name = 'Carte Cadeau 30min';

/* Select all Bundles
SELECT id, name, stripe_product_id, stripe_price_id FROM core_bundle;
*/

UPDATE core_bundle SET 
    stripe_product_id = 'prod_TF3BPyqDnT33bj',
    stripe_price_id = 'price_1SIZ5KIBHqwpYiZwxNnQfDuy' WHERE name = 'Forfait 10H';

UPDATE core_bundle SET 
    stripe_product_id = 'prod_TF3Cvru0cFqY9e',
    stripe_price_id = 'price_1SIZ6NIBHqwpYiZwnBPvbKEK' WHERE name = 'Forfait 5H';

UPDATE core_bundle SET 
    stripe_product_id = 'prod_TF3DMfXNoVlsSi',
    stripe_price_id = 'price_1SIZ6oIBHqwpYiZwjBCOgdDQ' WHERE name = 'Forfait 3H';
