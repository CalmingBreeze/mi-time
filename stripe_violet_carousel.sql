-- Restore product stripe correspondance id to test env from violet carousel
-- Use : in sqlite3 prompt : .read <filename>.sql

/* Select all giftcards
SELECT id, name, stripe_product_id, stripe_price_id, stripe_coupon_id FROM core_giftcard;
*/

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_T0hXrJp0sLfVX4',
    stripe_price_id = 'price_1S4g8bRhCpnOwUW3HOKYhDV7',
    stripe_coupon_id = '0iFn6IHX' WHERE name = 'Carte Cadeau 1h30';

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_SzbqH5Uq1Gt10D',
    stripe_price_id = 'price_1S3ccmRhCpnOwUW3Z6ocPlUJ',
    stripe_coupon_id = 'FWZTCZ0d' WHERE name = 'Carte Cadeau 1h';

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_T0oTTCkkDs3951',
    stripe_price_id = 'price_1S4mr1RhCpnOwUW3pZXqYJCv',
    stripe_coupon_id = 'crFrerdZ' WHERE name = 'Carte Cadeau 45min';

UPDATE core_giftcard SET 
    stripe_product_id = 'prod_T0oYyXlGm6SMa6',
    stripe_price_id = 'price_1S4mvQRhCpnOwUW3grrSpWCE',
    stripe_coupon_id = 'J5t3CXyY' WHERE name = 'Carte Cadeau 30min';

/* Select all Bundles
SELECT id, name, stripe_product_id, stripe_price_id FROM core_bundle;
*/

UPDATE core_bundle SET 
    stripe_product_id = 'prod_TFMLy9otrAoq8g',
    stripe_price_id = 'price_1SIrcyRhCpnOwUW3pAlj2929' WHERE name = 'Forfait 10H';

UPDATE core_bundle SET 
    stripe_product_id = 'prod_TFMMGEivtv5wXr',
    stripe_price_id = 'price_1SIrdKRhCpnOwUW3oKRGdfdc' WHERE name = 'Forfait 5H';

UPDATE core_bundle SET 
    stripe_product_id = 'prod_TFMMst6jHJFpwk',
    stripe_price_id = 'price_1SIrdgRhCpnOwUW3CliPoeZ2' WHERE name = 'Forfait 3H';