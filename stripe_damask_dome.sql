-- Restore product stripe correspondance id to test env from violet carousel
-- Use : in sqlite3 prompt : .read <filename>.sql

/* Select all giftcards
SELECT id, name, stripe_product_id, stripe_price_id, stripe_coupon_id FROM core_giftcard;
*/

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_TZxj1hRVncAKKa',
    stripe_price_id = 'price_1ScnnnRBrGMIS9RikmD8eE1K',
    stripe_coupon_id = 'tHEye624' WHERE name = 'Carte Cadeau 1h30';

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_TZxhPL2yphH22W',
    stripe_price_id = 'price_1ScnmVRBrGMIS9RimjAnqzAM',
    stripe_coupon_id = 'J38MpnLG' WHERE name = 'Carte Cadeau 1h';

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_TZxfcJlpbuhVzR',
    stripe_price_id = 'price_1ScnkaRBrGMIS9RiLlE7y8nB',
    stripe_coupon_id = 'UE5AcXSQ' WHERE name = 'Carte Cadeau 45min';

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_TZxbHYNgLmPDfJ',
    stripe_price_id = 'price_1Scng2RBrGMIS9RiH7xjTlQp',
    stripe_coupon_id = 'fLwzXXAO' WHERE name = 'Carte Cadeau 30min';

/* Select all Bundles
SELECT id, name, stripe_product_id, stripe_price_id FROM core_bundle;
*/

UPDATE core_bundle SET 
    stripe_product_id = 'prod_TZxZwY2JLVc3RP',
    stripe_price_id = 'price_1ScneaRBrGMIS9RiXONu9f3X' WHERE name = 'Forfait 10H';

UPDATE core_bundle SET 
    stripe_product_id = 'prod_TZxY9SljD0Xel0',
    stripe_price_id = 'price_1ScndlRBrGMIS9RiaG8O7IKP' WHERE name = 'Forfait 5H';

UPDATE core_bundle SET 
    stripe_product_id = 'prod_TZxXnTKjwwawQX',
    stripe_price_id = 'price_1ScnccRBrGMIS9Rib2eVT9jb' WHERE name = 'Forfait 3H';