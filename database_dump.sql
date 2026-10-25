--
-- PostgreSQL database dump
--

\restrict 3poeeSsl6IaWO3TNMf8pLtoeiyyzIX9bmcDUb0ij7zL5MNSLF7oR5uXwr2Cx9kw

-- Dumped from database version 16.15
-- Dumped by pg_dump version 16.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.payments_refundtransaction DROP CONSTRAINT IF EXISTS payments_refundtrans_payment_id_fd241ffa_fk_payments_;
ALTER TABLE IF EXISTS ONLY public.payments_refundtransaction DROP CONSTRAINT IF EXISTS payments_refundtrans_initiated_by_id_43c3e590_fk_accounts_;
ALTER TABLE IF EXISTS ONLY public.payments_paymentattempt DROP CONSTRAINT IF EXISTS payments_paymentattempt_order_id_d21442a3_fk_orders_order_id;
ALTER TABLE IF EXISTS ONLY public.payments_payment DROP CONSTRAINT IF EXISTS payments_payment_order_id_22c479b7_fk_orders_order_id;
ALTER TABLE IF EXISTS ONLY public.orders_shipment DROP CONSTRAINT IF EXISTS orders_shipment_order_id_661ed8ed_fk_orders_order_id;
ALTER TABLE IF EXISTS ONLY public.orders_returnrequest DROP CONSTRAINT IF EXISTS orders_returnrequest_user_id_38896318_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.orders_returnrequest DROP CONSTRAINT IF EXISTS orders_returnrequest_order_id_176addea_fk_orders_order_id;
ALTER TABLE IF EXISTS ONLY public.orders_orderstatushistory DROP CONSTRAINT IF EXISTS orders_orderstatushistory_order_id_bf09a0e1_fk_orders_order_id;
ALTER TABLE IF EXISTS ONLY public.orders_orderstatushistory DROP CONSTRAINT IF EXISTS orders_orderstatushi_changed_by_id_d823a516_fk_accounts_;
ALTER TABLE IF EXISTS ONLY public.orders_orderitem DROP CONSTRAINT IF EXISTS orders_orderitem_product_id_afe4254a_fk_catalog_product_id;
ALTER TABLE IF EXISTS ONLY public.orders_orderitem DROP CONSTRAINT IF EXISTS orders_orderitem_order_id_fe61a34d_fk_orders_order_id;
ALTER TABLE IF EXISTS ONLY public.orders_order DROP CONSTRAINT IF EXISTS orders_order_user_id_e9b59eb1_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.inventory_stockreservation DROP CONSTRAINT IF EXISTS inventory_stockreser_inventory_item_id_d06471c1_fk_inventory;
ALTER TABLE IF EXISTS ONLY public.inventory_stockmovement DROP CONSTRAINT IF EXISTS inventory_stockmovement_user_id_9fe5f98d_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.inventory_stockmovement DROP CONSTRAINT IF EXISTS inventory_stockmovem_inventory_item_id_b4825f9c_fk_inventory;
ALTER TABLE IF EXISTS ONLY public.inventory_inventoryitem DROP CONSTRAINT IF EXISTS inventory_inventoryi_variant_id_aa173510_fk_catalog_p;
ALTER TABLE IF EXISTS ONLY public.inventory_inventoryitem DROP CONSTRAINT IF EXISTS inventory_inventoryi_product_id_78574124_fk_catalog_p;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.discounts_couponredemption DROP CONSTRAINT IF EXISTS discounts_couponredemption_user_id_d1d15838_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.discounts_couponredemption DROP CONSTRAINT IF EXISTS discounts_couponrede_coupon_id_79fb0ae6_fk_discounts;
ALTER TABLE IF EXISTS ONLY public.core_auditlog DROP CONSTRAINT IF EXISTS core_auditlog_user_id_3797aaab_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.catalog_productvariant DROP CONSTRAINT IF EXISTS catalog_productvaria_product_id_422f9d19_fk_catalog_p;
ALTER TABLE IF EXISTS ONLY public.catalog_productreview DROP CONSTRAINT IF EXISTS catalog_productreview_user_id_b8f95029_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.catalog_productreview DROP CONSTRAINT IF EXISTS catalog_productreview_product_id_9407c0e9_fk_catalog_product_id;
ALTER TABLE IF EXISTS ONLY public.catalog_productimage DROP CONSTRAINT IF EXISTS catalog_productimage_product_id_1f42dd8c_fk_catalog_product_id;
ALTER TABLE IF EXISTS ONLY public.catalog_product DROP CONSTRAINT IF EXISTS catalog_product_category_id_35bf920b_fk_catalog_category_id;
ALTER TABLE IF EXISTS ONLY public.catalog_category DROP CONSTRAINT IF EXISTS catalog_category_parent_id_f61bd017_fk_catalog_category_id;
ALTER TABLE IF EXISTS ONLY public.cart_wishlistitem DROP CONSTRAINT IF EXISTS cart_wishlistitem_wishlist_id_dd2c2649_fk_cart_wishlist_id;
ALTER TABLE IF EXISTS ONLY public.cart_wishlistitem DROP CONSTRAINT IF EXISTS cart_wishlistitem_product_id_c183b0d4_fk_catalog_product_id;
ALTER TABLE IF EXISTS ONLY public.cart_wishlist DROP CONSTRAINT IF EXISTS cart_wishlist_user_id_c35eec54_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.cart_cartitem DROP CONSTRAINT IF EXISTS cart_cartitem_variant_id_69f5d8c8_fk_catalog_productvariant_id;
ALTER TABLE IF EXISTS ONLY public.cart_cartitem DROP CONSTRAINT IF EXISTS cart_cartitem_product_id_b24e265a_fk_catalog_product_id;
ALTER TABLE IF EXISTS ONLY public.cart_cartitem DROP CONSTRAINT IF EXISTS cart_cartitem_cart_id_370ad265_fk_cart_cart_id;
ALTER TABLE IF EXISTS ONLY public.cart_cart DROP CONSTRAINT IF EXISTS cart_cart_user_id_9b4220b9_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.accounts_userprofile DROP CONSTRAINT IF EXISTS accounts_userprofile_user_id_92240672_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.accounts_user_user_permissions DROP CONSTRAINT IF EXISTS accounts_user_user_p_user_id_e4f0a161_fk_accounts_;
ALTER TABLE IF EXISTS ONLY public.accounts_user_user_permissions DROP CONSTRAINT IF EXISTS accounts_user_user_p_permission_id_113bb443_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.accounts_user_groups DROP CONSTRAINT IF EXISTS accounts_user_groups_user_id_52b62117_fk_accounts_user_id;
ALTER TABLE IF EXISTS ONLY public.accounts_user_groups DROP CONSTRAINT IF EXISTS accounts_user_groups_group_id_bd11a704_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.accounts_customeraddress DROP CONSTRAINT IF EXISTS accounts_customeraddress_user_id_09d750f6_fk_accounts_user_id;
DROP INDEX IF EXISTS public.payments_refundtransaction_refund_id_a4cbbb91_like;
DROP INDEX IF EXISTS public.payments_refundtransaction_payment_id_fd241ffa;
DROP INDEX IF EXISTS public.payments_refundtransaction_initiated_by_id_43c3e590;
DROP INDEX IF EXISTS public.payments_refundtransaction_created_at_816a1611;
DROP INDEX IF EXISTS public.payments_paymentwebhookevent_is_processed_7f28835a;
DROP INDEX IF EXISTS public.payments_paymentwebhookevent_event_type_81be5efa_like;
DROP INDEX IF EXISTS public.payments_paymentwebhookevent_event_type_81be5efa;
DROP INDEX IF EXISTS public.payments_paymentwebhookevent_event_id_4ef43bcf_like;
DROP INDEX IF EXISTS public.payments_paymentwebhookevent_created_at_7bbd1526;
DROP INDEX IF EXISTS public.payments_paymentattempt_order_id_d21442a3;
DROP INDEX IF EXISTS public.payments_paymentattempt_gateway_order_id_a70e0911_like;
DROP INDEX IF EXISTS public.payments_paymentattempt_gateway_order_id_a70e0911;
DROP INDEX IF EXISTS public.payments_paymentattempt_created_at_92b002cb;
DROP INDEX IF EXISTS public.payments_payment_transaction_id_55f6af3a_like;
DROP INDEX IF EXISTS public.payments_payment_status_fc8cbda2_like;
DROP INDEX IF EXISTS public.payments_payment_status_fc8cbda2;
DROP INDEX IF EXISTS public.payments_payment_gateway_order_id_ebd789c6_like;
DROP INDEX IF EXISTS public.payments_payment_gateway_order_id_ebd789c6;
DROP INDEX IF EXISTS public.payments_payment_created_at_149046d5;
DROP INDEX IF EXISTS public.orders_shipment_created_at_e9b9b26d;
DROP INDEX IF EXISTS public.orders_returnrequest_user_id_38896318;
DROP INDEX IF EXISTS public.orders_returnrequest_order_id_176addea;
DROP INDEX IF EXISTS public.orders_returnrequest_created_at_002e2058;
DROP INDEX IF EXISTS public.orders_orderstatushistory_order_id_bf09a0e1;
DROP INDEX IF EXISTS public.orders_orderstatushistory_created_at_535f9788;
DROP INDEX IF EXISTS public.orders_orderstatushistory_changed_by_id_d823a516;
DROP INDEX IF EXISTS public.orders_orderitem_product_id_afe4254a;
DROP INDEX IF EXISTS public.orders_orderitem_order_id_fe61a34d;
DROP INDEX IF EXISTS public.orders_orderitem_created_at_9431be56;
DROP INDEX IF EXISTS public.orders_order_user_id_e9b59eb1;
DROP INDEX IF EXISTS public.orders_order_status_445594e5_like;
DROP INDEX IF EXISTS public.orders_order_status_445594e5;
DROP INDEX IF EXISTS public.orders_order_order_number_4e985f70_like;
DROP INDEX IF EXISTS public.orders_order_email_79665695_like;
DROP INDEX IF EXISTS public.orders_order_email_79665695;
DROP INDEX IF EXISTS public.orders_order_created_at_20b8d253;
DROP INDEX IF EXISTS public.inventory_stockreservation_reference_id_f2f456f8_like;
DROP INDEX IF EXISTS public.inventory_stockreservation_reference_id_f2f456f8;
DROP INDEX IF EXISTS public.inventory_stockreservation_is_released_bd40c130;
DROP INDEX IF EXISTS public.inventory_stockreservation_inventory_item_id_d06471c1;
DROP INDEX IF EXISTS public.inventory_stockreservation_created_at_f1993588;
DROP INDEX IF EXISTS public.inventory_stockmovement_user_id_9fe5f98d;
DROP INDEX IF EXISTS public.inventory_stockmovement_inventory_item_id_b4825f9c;
DROP INDEX IF EXISTS public.inventory_stockmovement_created_at_05b478ed;
DROP INDEX IF EXISTS public.inventory_inventoryitem_sku_9ccfd20b_like;
DROP INDEX IF EXISTS public.inventory_inventoryitem_created_at_5aba1a64;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.discounts_couponredemption_user_id_d1d15838;
DROP INDEX IF EXISTS public.discounts_couponredemption_order_id_b81e0bd1_like;
DROP INDEX IF EXISTS public.discounts_couponredemption_order_id_b81e0bd1;
DROP INDEX IF EXISTS public.discounts_couponredemption_created_at_26d8c3e4;
DROP INDEX IF EXISTS public.discounts_couponredemption_coupon_id_79fb0ae6;
DROP INDEX IF EXISTS public.discounts_coupon_is_active_f70e8c25;
DROP INDEX IF EXISTS public.discounts_coupon_created_at_6027ed69;
DROP INDEX IF EXISTS public.discounts_coupon_code_f0958380_like;
DROP INDEX IF EXISTS public.core_auditlog_user_id_3797aaab;
DROP INDEX IF EXISTS public.core_auditlog_timestamp_c6ef4463;
DROP INDEX IF EXISTS public.core_auditlog_resource_type_cb47b03d_like;
DROP INDEX IF EXISTS public.core_auditlog_resource_type_cb47b03d;
DROP INDEX IF EXISTS public.core_auditlog_action_978477aa_like;
DROP INDEX IF EXISTS public.core_auditlog_action_978477aa;
DROP INDEX IF EXISTS public.content_sitesetting_key_0508b562_like;
DROP INDEX IF EXISTS public.content_sitesetting_created_at_a32ed8d2;
DROP INDEX IF EXISTS public.content_page_slug_d48c800c_like;
DROP INDEX IF EXISTS public.content_page_is_published_8d0a35a7;
DROP INDEX IF EXISTS public.content_page_created_at_91c2ccd3;
DROP INDEX IF EXISTS public.content_newslettersubscription_email_ab9bfc1f_like;
DROP INDEX IF EXISTS public.content_newslettersubscription_created_at_2580bf8b;
DROP INDEX IF EXISTS public.content_banner_location_89e633bd_like;
DROP INDEX IF EXISTS public.content_banner_location_89e633bd;
DROP INDEX IF EXISTS public.content_banner_is_active_19606de5;
DROP INDEX IF EXISTS public.content_banner_created_at_24680f0b;
DROP INDEX IF EXISTS public.catalog_productvariant_sku_da81620a_like;
DROP INDEX IF EXISTS public.catalog_productvariant_product_id_422f9d19;
DROP INDEX IF EXISTS public.catalog_productvariant_created_at_525afd68;
DROP INDEX IF EXISTS public.catalog_productreview_user_id_b8f95029;
DROP INDEX IF EXISTS public.catalog_productreview_product_id_9407c0e9;
DROP INDEX IF EXISTS public.catalog_productreview_is_approved_603661d9;
DROP INDEX IF EXISTS public.catalog_productreview_created_at_4c042ca8;
DROP INDEX IF EXISTS public.catalog_productimage_product_id_1f42dd8c;
DROP INDEX IF EXISTS public.catalog_productimage_created_at_367e8076;
DROP INDEX IF EXISTS public.catalog_productattribute_slug_7a29bcb7_like;
DROP INDEX IF EXISTS public.catalog_productattribute_name_6fe00e8b_like;
DROP INDEX IF EXISTS public.catalog_productattribute_created_at_53411af8;
DROP INDEX IF EXISTS public.catalog_product_slug_f37848b0_like;
DROP INDEX IF EXISTS public.catalog_product_sku_5c54c070_like;
DROP INDEX IF EXISTS public.catalog_product_price_1347cb30;
DROP INDEX IF EXISTS public.catalog_product_name_924af5bc_like;
DROP INDEX IF EXISTS public.catalog_product_name_924af5bc;
DROP INDEX IF EXISTS public.catalog_product_is_trending_33a3a09e;
DROP INDEX IF EXISTS public.catalog_product_is_new_arrival_eef7e0fb;
DROP INDEX IF EXISTS public.catalog_product_is_featured_4286e684;
DROP INDEX IF EXISTS public.catalog_product_is_archived_cd365c0e;
DROP INDEX IF EXISTS public.catalog_product_is_active_6ce66e03;
DROP INDEX IF EXISTS public.catalog_product_created_at_ea90ae72;
DROP INDEX IF EXISTS public.catalog_product_category_id_35bf920b;
DROP INDEX IF EXISTS public.catalog_category_slug_dbf63ad0_like;
DROP INDEX IF EXISTS public.catalog_category_parent_id_f61bd017;
DROP INDEX IF EXISTS public.catalog_category_name_fdc3466c_like;
DROP INDEX IF EXISTS public.catalog_category_is_featured_efab636a;
DROP INDEX IF EXISTS public.catalog_category_is_active_66b33fbf;
DROP INDEX IF EXISTS public.catalog_category_created_at_2f95ea55;
DROP INDEX IF EXISTS public.cart_wishlistitem_wishlist_id_dd2c2649;
DROP INDEX IF EXISTS public.cart_wishlistitem_product_id_c183b0d4;
DROP INDEX IF EXISTS public.cart_wishlistitem_created_at_0a951113;
DROP INDEX IF EXISTS public.cart_wishlist_created_at_87ebfab4;
DROP INDEX IF EXISTS public.cart_cartitem_variant_id_69f5d8c8;
DROP INDEX IF EXISTS public.cart_cartitem_product_id_b24e265a;
DROP INDEX IF EXISTS public.cart_cartitem_created_at_f0361bf9;
DROP INDEX IF EXISTS public.cart_cartitem_cart_id_370ad265;
DROP INDEX IF EXISTS public.cart_cart_user_id_9b4220b9;
DROP INDEX IF EXISTS public.cart_cart_session_key_bf21cb35_like;
DROP INDEX IF EXISTS public.cart_cart_session_key_bf21cb35;
DROP INDEX IF EXISTS public.cart_cart_created_at_82800f17;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
DROP INDEX IF EXISTS public.accounts_userprofile_created_at_0f764602;
DROP INDEX IF EXISTS public.accounts_user_user_permissions_user_id_e4f0a161;
DROP INDEX IF EXISTS public.accounts_user_user_permissions_permission_id_113bb443;
DROP INDEX IF EXISTS public.accounts_user_role_57e97df0_like;
DROP INDEX IF EXISTS public.accounts_user_role_57e97df0;
DROP INDEX IF EXISTS public.accounts_user_groups_user_id_52b62117;
DROP INDEX IF EXISTS public.accounts_user_groups_group_id_bd11a704;
DROP INDEX IF EXISTS public.accounts_user_email_b2644a56_like;
DROP INDEX IF EXISTS public.accounts_customeraddress_user_id_09d750f6;
DROP INDEX IF EXISTS public.accounts_customeraddress_created_at_84b947d5;
ALTER TABLE IF EXISTS ONLY public.payments_refundtransaction DROP CONSTRAINT IF EXISTS payments_refundtransaction_refund_id_key;
ALTER TABLE IF EXISTS ONLY public.payments_refundtransaction DROP CONSTRAINT IF EXISTS payments_refundtransaction_pkey;
ALTER TABLE IF EXISTS ONLY public.payments_paymentwebhookevent DROP CONSTRAINT IF EXISTS payments_paymentwebhookevent_pkey;
ALTER TABLE IF EXISTS ONLY public.payments_paymentwebhookevent DROP CONSTRAINT IF EXISTS payments_paymentwebhookevent_event_id_key;
ALTER TABLE IF EXISTS ONLY public.payments_paymentattempt DROP CONSTRAINT IF EXISTS payments_paymentattempt_pkey;
ALTER TABLE IF EXISTS ONLY public.payments_payment DROP CONSTRAINT IF EXISTS payments_payment_transaction_id_key;
ALTER TABLE IF EXISTS ONLY public.payments_payment DROP CONSTRAINT IF EXISTS payments_payment_pkey;
ALTER TABLE IF EXISTS ONLY public.payments_payment DROP CONSTRAINT IF EXISTS payments_payment_order_id_key;
ALTER TABLE IF EXISTS ONLY public.orders_shipment DROP CONSTRAINT IF EXISTS orders_shipment_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_shipment DROP CONSTRAINT IF EXISTS orders_shipment_order_id_key;
ALTER TABLE IF EXISTS ONLY public.orders_returnrequest DROP CONSTRAINT IF EXISTS orders_returnrequest_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_orderstatushistory DROP CONSTRAINT IF EXISTS orders_orderstatushistory_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_orderitem DROP CONSTRAINT IF EXISTS orders_orderitem_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_order DROP CONSTRAINT IF EXISTS orders_order_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_order DROP CONSTRAINT IF EXISTS orders_order_order_number_key;
ALTER TABLE IF EXISTS ONLY public.inventory_stockreservation DROP CONSTRAINT IF EXISTS inventory_stockreservation_pkey;
ALTER TABLE IF EXISTS ONLY public.inventory_stockmovement DROP CONSTRAINT IF EXISTS inventory_stockmovement_pkey;
ALTER TABLE IF EXISTS ONLY public.inventory_inventoryitem DROP CONSTRAINT IF EXISTS inventory_inventoryitem_variant_id_key;
ALTER TABLE IF EXISTS ONLY public.inventory_inventoryitem DROP CONSTRAINT IF EXISTS inventory_inventoryitem_sku_key;
ALTER TABLE IF EXISTS ONLY public.inventory_inventoryitem DROP CONSTRAINT IF EXISTS inventory_inventoryitem_product_id_key;
ALTER TABLE IF EXISTS ONLY public.inventory_inventoryitem DROP CONSTRAINT IF EXISTS inventory_inventoryitem_pkey;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.discounts_couponredemption DROP CONSTRAINT IF EXISTS discounts_couponredemption_pkey;
ALTER TABLE IF EXISTS ONLY public.discounts_coupon DROP CONSTRAINT IF EXISTS discounts_coupon_pkey;
ALTER TABLE IF EXISTS ONLY public.discounts_coupon DROP CONSTRAINT IF EXISTS discounts_coupon_code_key;
ALTER TABLE IF EXISTS ONLY public.core_auditlog DROP CONSTRAINT IF EXISTS core_auditlog_pkey;
ALTER TABLE IF EXISTS ONLY public.content_sitesetting DROP CONSTRAINT IF EXISTS content_sitesetting_pkey;
ALTER TABLE IF EXISTS ONLY public.content_sitesetting DROP CONSTRAINT IF EXISTS content_sitesetting_key_key;
ALTER TABLE IF EXISTS ONLY public.content_page DROP CONSTRAINT IF EXISTS content_page_slug_key;
ALTER TABLE IF EXISTS ONLY public.content_page DROP CONSTRAINT IF EXISTS content_page_pkey;
ALTER TABLE IF EXISTS ONLY public.content_newslettersubscription DROP CONSTRAINT IF EXISTS content_newslettersubscription_pkey;
ALTER TABLE IF EXISTS ONLY public.content_newslettersubscription DROP CONSTRAINT IF EXISTS content_newslettersubscription_email_key;
ALTER TABLE IF EXISTS ONLY public.content_banner DROP CONSTRAINT IF EXISTS content_banner_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_productvariant DROP CONSTRAINT IF EXISTS catalog_productvariant_sku_key;
ALTER TABLE IF EXISTS ONLY public.catalog_productvariant DROP CONSTRAINT IF EXISTS catalog_productvariant_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_productreview DROP CONSTRAINT IF EXISTS catalog_productreview_product_id_user_id_4c0fbc41_uniq;
ALTER TABLE IF EXISTS ONLY public.catalog_productreview DROP CONSTRAINT IF EXISTS catalog_productreview_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_productimage DROP CONSTRAINT IF EXISTS catalog_productimage_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_productattribute DROP CONSTRAINT IF EXISTS catalog_productattribute_slug_key;
ALTER TABLE IF EXISTS ONLY public.catalog_productattribute DROP CONSTRAINT IF EXISTS catalog_productattribute_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_productattribute DROP CONSTRAINT IF EXISTS catalog_productattribute_name_key;
ALTER TABLE IF EXISTS ONLY public.catalog_product DROP CONSTRAINT IF EXISTS catalog_product_slug_key;
ALTER TABLE IF EXISTS ONLY public.catalog_product DROP CONSTRAINT IF EXISTS catalog_product_sku_key;
ALTER TABLE IF EXISTS ONLY public.catalog_product DROP CONSTRAINT IF EXISTS catalog_product_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_category DROP CONSTRAINT IF EXISTS catalog_category_slug_key;
ALTER TABLE IF EXISTS ONLY public.catalog_category DROP CONSTRAINT IF EXISTS catalog_category_pkey;
ALTER TABLE IF EXISTS ONLY public.catalog_category DROP CONSTRAINT IF EXISTS catalog_category_name_key;
ALTER TABLE IF EXISTS ONLY public.cart_wishlistitem DROP CONSTRAINT IF EXISTS cart_wishlistitem_wishlist_id_product_id_ec03f6f6_uniq;
ALTER TABLE IF EXISTS ONLY public.cart_wishlistitem DROP CONSTRAINT IF EXISTS cart_wishlistitem_pkey;
ALTER TABLE IF EXISTS ONLY public.cart_wishlist DROP CONSTRAINT IF EXISTS cart_wishlist_user_id_key;
ALTER TABLE IF EXISTS ONLY public.cart_wishlist DROP CONSTRAINT IF EXISTS cart_wishlist_pkey;
ALTER TABLE IF EXISTS ONLY public.cart_cartitem DROP CONSTRAINT IF EXISTS cart_cartitem_pkey;
ALTER TABLE IF EXISTS ONLY public.cart_cartitem DROP CONSTRAINT IF EXISTS cart_cartitem_cart_id_product_id_variant_id_5fc0c5f3_uniq;
ALTER TABLE IF EXISTS ONLY public.cart_cart DROP CONSTRAINT IF EXISTS cart_cart_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
ALTER TABLE IF EXISTS ONLY public.accounts_userprofile DROP CONSTRAINT IF EXISTS accounts_userprofile_user_id_key;
ALTER TABLE IF EXISTS ONLY public.accounts_userprofile DROP CONSTRAINT IF EXISTS accounts_userprofile_pkey;
ALTER TABLE IF EXISTS ONLY public.accounts_user_user_permissions DROP CONSTRAINT IF EXISTS accounts_user_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.accounts_user_user_permissions DROP CONSTRAINT IF EXISTS accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq;
ALTER TABLE IF EXISTS ONLY public.accounts_user DROP CONSTRAINT IF EXISTS accounts_user_pkey;
ALTER TABLE IF EXISTS ONLY public.accounts_user_groups DROP CONSTRAINT IF EXISTS accounts_user_groups_user_id_group_id_59c0b32f_uniq;
ALTER TABLE IF EXISTS ONLY public.accounts_user_groups DROP CONSTRAINT IF EXISTS accounts_user_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.accounts_user DROP CONSTRAINT IF EXISTS accounts_user_email_key;
ALTER TABLE IF EXISTS ONLY public.accounts_customeraddress DROP CONSTRAINT IF EXISTS accounts_customeraddress_pkey;
DROP TABLE IF EXISTS public.payments_refundtransaction;
DROP TABLE IF EXISTS public.payments_paymentwebhookevent;
DROP TABLE IF EXISTS public.payments_paymentattempt;
DROP TABLE IF EXISTS public.payments_payment;
DROP TABLE IF EXISTS public.orders_shipment;
DROP TABLE IF EXISTS public.orders_returnrequest;
DROP TABLE IF EXISTS public.orders_orderstatushistory;
DROP TABLE IF EXISTS public.orders_orderitem;
DROP TABLE IF EXISTS public.orders_order;
DROP TABLE IF EXISTS public.inventory_stockreservation;
DROP TABLE IF EXISTS public.inventory_stockmovement;
DROP TABLE IF EXISTS public.inventory_inventoryitem;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.discounts_couponredemption;
DROP TABLE IF EXISTS public.discounts_coupon;
DROP TABLE IF EXISTS public.core_auditlog;
DROP TABLE IF EXISTS public.content_sitesetting;
DROP TABLE IF EXISTS public.content_page;
DROP TABLE IF EXISTS public.content_newslettersubscription;
DROP TABLE IF EXISTS public.content_banner;
DROP TABLE IF EXISTS public.catalog_productvariant;
DROP TABLE IF EXISTS public.catalog_productreview;
DROP TABLE IF EXISTS public.catalog_productimage;
DROP TABLE IF EXISTS public.catalog_productattribute;
DROP TABLE IF EXISTS public.catalog_product;
DROP TABLE IF EXISTS public.catalog_category;
DROP TABLE IF EXISTS public.cart_wishlistitem;
DROP TABLE IF EXISTS public.cart_wishlist;
DROP TABLE IF EXISTS public.cart_cartitem;
DROP TABLE IF EXISTS public.cart_cart;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
DROP TABLE IF EXISTS public.accounts_userprofile;
DROP TABLE IF EXISTS public.accounts_user_user_permissions;
DROP TABLE IF EXISTS public.accounts_user_groups;
DROP TABLE IF EXISTS public.accounts_user;
DROP TABLE IF EXISTS public.accounts_customeraddress;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: accounts_customeraddress; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.accounts_customeraddress (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    full_name character varying(150) NOT NULL,
    phone character varying(20) NOT NULL,
    address_line_1 character varying(255) NOT NULL,
    address_line_2 character varying(255) NOT NULL,
    city character varying(100) NOT NULL,
    state character varying(100) NOT NULL,
    postal_code character varying(20) NOT NULL,
    country character varying(100) NOT NULL,
    address_type character varying(15) NOT NULL,
    is_default boolean NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.accounts_customeraddress OWNER TO "ZIYO";

--
-- Name: accounts_user; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.accounts_user (
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    id uuid NOT NULL,
    email character varying(254) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    phone character varying(20) NOT NULL,
    role character varying(20) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.accounts_user OWNER TO "ZIYO";

--
-- Name: accounts_user_groups; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.accounts_user_groups (
    id bigint NOT NULL,
    user_id uuid NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.accounts_user_groups OWNER TO "ZIYO";

--
-- Name: accounts_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: ZIYO
--

ALTER TABLE public.accounts_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: accounts_user_user_permissions; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.accounts_user_user_permissions (
    id bigint NOT NULL,
    user_id uuid NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.accounts_user_user_permissions OWNER TO "ZIYO";

--
-- Name: accounts_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: ZIYO
--

ALTER TABLE public.accounts_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: accounts_userprofile; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.accounts_userprofile (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    avatar character varying(100),
    bio text NOT NULL,
    birth_date date,
    newsletter_subscribed boolean NOT NULL,
    loyalty_points integer NOT NULL,
    preferred_currency character varying(3) NOT NULL,
    user_id uuid NOT NULL,
    CONSTRAINT accounts_userprofile_loyalty_points_check CHECK ((loyalty_points >= 0))
);


ALTER TABLE public.accounts_userprofile OWNER TO "ZIYO";

--
-- Name: accounts_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: ZIYO
--

ALTER TABLE public.accounts_userprofile ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_userprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO "ZIYO";

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: ZIYO
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO "ZIYO";

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: ZIYO
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO "ZIYO";

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: ZIYO
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cart_cart; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.cart_cart (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    session_key character varying(80),
    user_id uuid
);


ALTER TABLE public.cart_cart OWNER TO "ZIYO";

--
-- Name: cart_cartitem; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.cart_cartitem (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    quantity integer NOT NULL,
    cart_id uuid NOT NULL,
    product_id uuid NOT NULL,
    variant_id uuid,
    CONSTRAINT cart_cartitem_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.cart_cartitem OWNER TO "ZIYO";

--
-- Name: cart_wishlist; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.cart_wishlist (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.cart_wishlist OWNER TO "ZIYO";

--
-- Name: cart_wishlistitem; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.cart_wishlistitem (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    product_id uuid NOT NULL,
    wishlist_id uuid NOT NULL
);


ALTER TABLE public.cart_wishlistitem OWNER TO "ZIYO";

--
-- Name: catalog_category; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.catalog_category (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    name character varying(150) NOT NULL,
    slug character varying(180) NOT NULL,
    description text NOT NULL,
    image character varying(100),
    is_featured boolean NOT NULL,
    is_active boolean NOT NULL,
    sort_order integer NOT NULL,
    parent_id uuid,
    CONSTRAINT catalog_category_sort_order_check CHECK ((sort_order >= 0))
);


ALTER TABLE public.catalog_category OWNER TO "ZIYO";

--
-- Name: catalog_product; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.catalog_product (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(280) NOT NULL,
    sku character varying(80) NOT NULL,
    short_description character varying(300) NOT NULL,
    description text NOT NULL,
    price numeric(12,2) NOT NULL,
    compare_at_price numeric(12,2),
    cost_price numeric(12,2),
    is_featured boolean NOT NULL,
    is_trending boolean NOT NULL,
    is_new_arrival boolean NOT NULL,
    is_active boolean NOT NULL,
    is_archived boolean NOT NULL,
    tags character varying(255) NOT NULL,
    category_id uuid NOT NULL
);


ALTER TABLE public.catalog_product OWNER TO "ZIYO";

--
-- Name: catalog_productattribute; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.catalog_productattribute (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name character varying(80) NOT NULL,
    slug character varying(100) NOT NULL
);


ALTER TABLE public.catalog_productattribute OWNER TO "ZIYO";

--
-- Name: catalog_productattribute_id_seq; Type: SEQUENCE; Schema: public; Owner: ZIYO
--

ALTER TABLE public.catalog_productattribute ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.catalog_productattribute_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: catalog_productimage; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.catalog_productimage (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    image character varying(100) NOT NULL,
    alt_text character varying(255) NOT NULL,
    is_feature boolean NOT NULL,
    sort_order integer NOT NULL,
    product_id uuid NOT NULL,
    CONSTRAINT catalog_productimage_sort_order_check CHECK ((sort_order >= 0))
);


ALTER TABLE public.catalog_productimage OWNER TO "ZIYO";

--
-- Name: catalog_productreview; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.catalog_productreview (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    rating smallint NOT NULL,
    title character varying(150) NOT NULL,
    comment text NOT NULL,
    is_approved boolean NOT NULL,
    product_id uuid NOT NULL,
    user_id uuid NOT NULL,
    CONSTRAINT catalog_productreview_rating_check CHECK ((rating >= 0))
);


ALTER TABLE public.catalog_productreview OWNER TO "ZIYO";

--
-- Name: catalog_productvariant; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.catalog_productvariant (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    name character varying(150) NOT NULL,
    sku character varying(80) NOT NULL,
    price_override numeric(12,2),
    attributes jsonb NOT NULL,
    is_active boolean NOT NULL,
    product_id uuid NOT NULL
);


ALTER TABLE public.catalog_productvariant OWNER TO "ZIYO";

--
-- Name: content_banner; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.content_banner (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    title character varying(200) NOT NULL,
    subtitle character varying(255) NOT NULL,
    image character varying(100),
    link_url character varying(255) NOT NULL,
    button_text character varying(50) NOT NULL,
    location character varying(25) NOT NULL,
    is_active boolean NOT NULL,
    sort_order integer NOT NULL,
    CONSTRAINT content_banner_sort_order_check CHECK ((sort_order >= 0))
);


ALTER TABLE public.content_banner OWNER TO "ZIYO";

--
-- Name: content_newslettersubscription; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.content_newslettersubscription (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    email character varying(254) NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.content_newslettersubscription OWNER TO "ZIYO";

--
-- Name: content_newslettersubscription_id_seq; Type: SEQUENCE; Schema: public; Owner: ZIYO
--

ALTER TABLE public.content_newslettersubscription ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.content_newslettersubscription_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: content_page; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.content_page (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    title character varying(200) NOT NULL,
    slug character varying(220) NOT NULL,
    content text NOT NULL,
    meta_description character varying(255) NOT NULL,
    is_published boolean NOT NULL
);


ALTER TABLE public.content_page OWNER TO "ZIYO";

--
-- Name: content_sitesetting; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.content_sitesetting (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    key character varying(80) NOT NULL,
    value text NOT NULL,
    description character varying(255) NOT NULL
);


ALTER TABLE public.content_sitesetting OWNER TO "ZIYO";

--
-- Name: content_sitesetting_id_seq; Type: SEQUENCE; Schema: public; Owner: ZIYO
--

ALTER TABLE public.content_sitesetting ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.content_sitesetting_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: core_auditlog; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.core_auditlog (
    id uuid NOT NULL,
    user_email character varying(254) NOT NULL,
    action character varying(40) NOT NULL,
    resource_type character varying(80) NOT NULL,
    resource_id character varying(120) NOT NULL,
    ip_address inet,
    user_agent character varying(255) NOT NULL,
    details jsonb NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    user_id uuid
);


ALTER TABLE public.core_auditlog OWNER TO "ZIYO";

--
-- Name: discounts_coupon; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.discounts_coupon (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    code character varying(30) NOT NULL,
    discount_type character varying(20) NOT NULL,
    value numeric(10,2) NOT NULL,
    min_purchase_amount numeric(12,2) NOT NULL,
    max_discount_amount numeric(12,2),
    usage_limit integer,
    per_user_limit integer NOT NULL,
    used_count integer NOT NULL,
    valid_from timestamp with time zone NOT NULL,
    valid_to timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    CONSTRAINT discounts_coupon_per_user_limit_check CHECK ((per_user_limit >= 0)),
    CONSTRAINT discounts_coupon_usage_limit_check CHECK ((usage_limit >= 0)),
    CONSTRAINT discounts_coupon_used_count_check CHECK ((used_count >= 0))
);


ALTER TABLE public.discounts_coupon OWNER TO "ZIYO";

--
-- Name: discounts_couponredemption; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.discounts_couponredemption (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    order_id character varying(120) NOT NULL,
    discount_amount numeric(12,2) NOT NULL,
    coupon_id uuid NOT NULL,
    user_id uuid
);


ALTER TABLE public.discounts_couponredemption OWNER TO "ZIYO";

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id uuid NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO "ZIYO";

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: ZIYO
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO "ZIYO";

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: ZIYO
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO "ZIYO";

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: ZIYO
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO "ZIYO";

--
-- Name: inventory_inventoryitem; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.inventory_inventoryitem (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    sku character varying(80) NOT NULL,
    quantity_on_hand integer NOT NULL,
    reserved_quantity integer NOT NULL,
    low_stock_threshold integer NOT NULL,
    product_id uuid,
    variant_id uuid,
    CONSTRAINT inventory_inventoryitem_low_stock_threshold_check CHECK ((low_stock_threshold >= 0)),
    CONSTRAINT inventory_inventoryitem_quantity_on_hand_check CHECK ((quantity_on_hand >= 0)),
    CONSTRAINT inventory_inventoryitem_reserved_quantity_check CHECK ((reserved_quantity >= 0))
);


ALTER TABLE public.inventory_inventoryitem OWNER TO "ZIYO";

--
-- Name: inventory_stockmovement; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.inventory_stockmovement (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    movement_type character varying(30) NOT NULL,
    quantity integer NOT NULL,
    reference_id character varying(120) NOT NULL,
    notes character varying(255) NOT NULL,
    inventory_item_id uuid NOT NULL,
    user_id uuid
);


ALTER TABLE public.inventory_stockmovement OWNER TO "ZIYO";

--
-- Name: inventory_stockreservation; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.inventory_stockreservation (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    quantity integer NOT NULL,
    reference_id character varying(120) NOT NULL,
    is_released boolean NOT NULL,
    inventory_item_id uuid NOT NULL,
    CONSTRAINT inventory_stockreservation_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.inventory_stockreservation OWNER TO "ZIYO";

--
-- Name: orders_order; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.orders_order (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    order_number character varying(40) NOT NULL,
    email character varying(254) NOT NULL,
    phone character varying(20) NOT NULL,
    status character varying(20) NOT NULL,
    subtotal numeric(12,2) NOT NULL,
    discount_amount numeric(12,2) NOT NULL,
    coupon_code character varying(50) NOT NULL,
    shipping_fee numeric(12,2) NOT NULL,
    tax_amount numeric(12,2) NOT NULL,
    total_amount numeric(12,2) NOT NULL,
    shipping_full_name character varying(150) NOT NULL,
    shipping_phone character varying(20) NOT NULL,
    shipping_address_line_1 character varying(255) NOT NULL,
    shipping_address_line_2 character varying(255) NOT NULL,
    shipping_city character varying(100) NOT NULL,
    shipping_state character varying(100) NOT NULL,
    shipping_postal_code character varying(20) NOT NULL,
    shipping_country character varying(100) NOT NULL,
    customer_notes text NOT NULL,
    admin_notes text NOT NULL,
    tracking_number character varying(100) NOT NULL,
    carrier character varying(100) NOT NULL,
    user_id uuid
);


ALTER TABLE public.orders_order OWNER TO "ZIYO";

--
-- Name: orders_orderitem; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.orders_orderitem (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    product_name character varying(255) NOT NULL,
    variant_name character varying(150) NOT NULL,
    sku character varying(80) NOT NULL,
    unit_price numeric(12,2) NOT NULL,
    quantity integer NOT NULL,
    line_total numeric(12,2) NOT NULL,
    order_id uuid NOT NULL,
    product_id uuid,
    CONSTRAINT orders_orderitem_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.orders_orderitem OWNER TO "ZIYO";

--
-- Name: orders_orderstatushistory; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.orders_orderstatushistory (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    status character varying(25) NOT NULL,
    notes character varying(255) NOT NULL,
    changed_by_id uuid,
    order_id uuid NOT NULL
);


ALTER TABLE public.orders_orderstatushistory OWNER TO "ZIYO";

--
-- Name: orders_returnrequest; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.orders_returnrequest (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    reason text NOT NULL,
    status character varying(20) NOT NULL,
    admin_notes text NOT NULL,
    order_id uuid NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.orders_returnrequest OWNER TO "ZIYO";

--
-- Name: orders_shipment; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.orders_shipment (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    carrier character varying(100) NOT NULL,
    tracking_number character varying(120) NOT NULL,
    shipped_at timestamp with time zone NOT NULL,
    estimated_delivery date,
    order_id uuid NOT NULL
);


ALTER TABLE public.orders_shipment OWNER TO "ZIYO";

--
-- Name: payments_payment; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.payments_payment (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    provider character varying(30) NOT NULL,
    transaction_id character varying(120) NOT NULL,
    gateway_order_id character varying(120) NOT NULL,
    amount numeric(12,2) NOT NULL,
    currency character varying(10) NOT NULL,
    status character varying(20) NOT NULL,
    payment_method_type character varying(50) NOT NULL,
    raw_response jsonb NOT NULL,
    order_id uuid NOT NULL
);


ALTER TABLE public.payments_payment OWNER TO "ZIYO";

--
-- Name: payments_paymentattempt; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.payments_paymentattempt (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    gateway_order_id character varying(120) NOT NULL,
    status character varying(30) NOT NULL,
    error_code character varying(100) NOT NULL,
    error_description text NOT NULL,
    order_id uuid NOT NULL
);


ALTER TABLE public.payments_paymentattempt OWNER TO "ZIYO";

--
-- Name: payments_paymentwebhookevent; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.payments_paymentwebhookevent (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    event_id character varying(150) NOT NULL,
    event_type character varying(100) NOT NULL,
    provider character varying(30) NOT NULL,
    payload jsonb NOT NULL,
    is_processed boolean NOT NULL,
    processed_at timestamp with time zone
);


ALTER TABLE public.payments_paymentwebhookevent OWNER TO "ZIYO";

--
-- Name: payments_refundtransaction; Type: TABLE; Schema: public; Owner: ZIYO
--

CREATE TABLE public.payments_refundtransaction (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    refund_id character varying(120) NOT NULL,
    amount numeric(12,2) NOT NULL,
    reason character varying(255) NOT NULL,
    status character varying(30) NOT NULL,
    initiated_by_id uuid,
    payment_id uuid NOT NULL
);


ALTER TABLE public.payments_refundtransaction OWNER TO "ZIYO";

--
-- Data for Name: accounts_customeraddress; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.accounts_customeraddress (created_at, updated_at, id, full_name, phone, address_line_1, address_line_2, city, state, postal_code, country, address_type, is_default, user_id) FROM stdin;
\.


--
-- Data for Name: accounts_user; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.accounts_user (password, last_login, is_superuser, id, email, first_name, last_name, phone, role, is_staff, is_active, date_joined) FROM stdin;
pbkdf2_sha256$870000$kkttaYKQ8zgt6VCcXxj9J3$DWg3TVd1NqWXRs67DcH2BhmnBLuFEPIMNXTHPbvCgA8=	\N	t	0af88137-9f73-4f4e-83a8-41916b7aa839	ziyo@ziyo.store	ZIYO			SUPERUSER	t	t	2026-10-25 23:15:58.116595+05:30
pbkdf2_sha256$870000$CAWuCK8etvQ63HyYQetGFB$mk305414/6ZnOTg4KWkjTkYAD1FxBgKp++6uycgFnbk=	2026-10-25 23:26:34.216121+05:30	t	ecd7b997-806a-418b-854b-5943e5a95f92	ziyo@example.com	Ziyo	Admin		SUPERUSER	t	t	2026-10-25 22:14:07.935611+05:30
\.


--
-- Data for Name: accounts_user_groups; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.accounts_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: accounts_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.accounts_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: accounts_userprofile; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.accounts_userprofile (id, created_at, updated_at, avatar, bio, birth_date, newsletter_subscribed, loyalty_points, preferred_currency, user_id) FROM stdin;
2	2026-10-25 23:15:58.117783+05:30	2026-10-25 23:15:58.502491+05:30			\N	t	0	INR	0af88137-9f73-4f4e-83a8-41916b7aa839
1	2026-10-25 22:14:07.937009+05:30	2026-10-25 23:26:34.21922+05:30			\N	t	0	INR	ecd7b997-806a-418b-854b-5943e5a95f92
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add Audit Log	6	add_auditlog
22	Can change Audit Log	6	change_auditlog
23	Can delete Audit Log	6	delete_auditlog
24	Can view Audit Log	6	view_auditlog
25	Can add User	7	add_user
26	Can change User	7	change_user
27	Can delete User	7	delete_user
28	Can view User	7	view_user
29	Can add Customer Address	8	add_customeraddress
30	Can change Customer Address	8	change_customeraddress
31	Can delete Customer Address	8	delete_customeraddress
32	Can view Customer Address	8	view_customeraddress
33	Can add user profile	9	add_userprofile
34	Can change user profile	9	change_userprofile
35	Can delete user profile	9	delete_userprofile
36	Can view user profile	9	view_userprofile
37	Can add product attribute	10	add_productattribute
38	Can change product attribute	10	change_productattribute
39	Can delete product attribute	10	delete_productattribute
40	Can view product attribute	10	view_productattribute
41	Can add Category	11	add_category
42	Can change Category	11	change_category
43	Can delete Category	11	delete_category
44	Can view Category	11	view_category
45	Can add Product	12	add_product
46	Can change Product	12	change_product
47	Can delete Product	12	delete_product
48	Can view Product	12	view_product
49	Can add product image	13	add_productimage
50	Can change product image	13	change_productimage
51	Can delete product image	13	delete_productimage
52	Can view product image	13	view_productimage
53	Can add product variant	14	add_productvariant
54	Can change product variant	14	change_productvariant
55	Can delete product variant	14	delete_productvariant
56	Can view product variant	14	view_productvariant
57	Can add product review	15	add_productreview
58	Can change product review	15	change_productreview
59	Can delete product review	15	delete_productreview
60	Can view product review	15	view_productreview
61	Can add Inventory Item	16	add_inventoryitem
62	Can change Inventory Item	16	change_inventoryitem
63	Can delete Inventory Item	16	delete_inventoryitem
64	Can view Inventory Item	16	view_inventoryitem
65	Can add Stock Movement	17	add_stockmovement
66	Can change Stock Movement	17	change_stockmovement
67	Can delete Stock Movement	17	delete_stockmovement
68	Can view Stock Movement	17	view_stockmovement
69	Can add stock reservation	18	add_stockreservation
70	Can change stock reservation	18	change_stockreservation
71	Can delete stock reservation	18	delete_stockreservation
72	Can view stock reservation	18	view_stockreservation
73	Can add cart	19	add_cart
74	Can change cart	19	change_cart
75	Can delete cart	19	delete_cart
76	Can view cart	19	view_cart
77	Can add wishlist	20	add_wishlist
78	Can change wishlist	20	change_wishlist
79	Can delete wishlist	20	delete_wishlist
80	Can view wishlist	20	view_wishlist
81	Can add cart item	21	add_cartitem
82	Can change cart item	21	change_cartitem
83	Can delete cart item	21	delete_cartitem
84	Can view cart item	21	view_cartitem
85	Can add wishlist item	22	add_wishlistitem
86	Can change wishlist item	22	change_wishlistitem
87	Can delete wishlist item	22	delete_wishlistitem
88	Can view wishlist item	22	view_wishlistitem
89	Can add Order	23	add_order
90	Can change Order	23	change_order
91	Can delete Order	23	delete_order
92	Can view Order	23	view_order
93	Can add order item	24	add_orderitem
94	Can change order item	24	change_orderitem
95	Can delete order item	24	delete_orderitem
96	Can view order item	24	view_orderitem
97	Can add Order Status History	25	add_orderstatushistory
98	Can change Order Status History	25	change_orderstatushistory
99	Can delete Order Status History	25	delete_orderstatushistory
100	Can view Order Status History	25	view_orderstatushistory
101	Can add return request	26	add_returnrequest
102	Can change return request	26	change_returnrequest
103	Can delete return request	26	delete_returnrequest
104	Can view return request	26	view_returnrequest
105	Can add shipment	27	add_shipment
106	Can change shipment	27	change_shipment
107	Can delete shipment	27	delete_shipment
108	Can view shipment	27	view_shipment
109	Can add payment webhook event	28	add_paymentwebhookevent
110	Can change payment webhook event	28	change_paymentwebhookevent
111	Can delete payment webhook event	28	delete_paymentwebhookevent
112	Can view payment webhook event	28	view_paymentwebhookevent
113	Can add Payment	29	add_payment
114	Can change Payment	29	change_payment
115	Can delete Payment	29	delete_payment
116	Can view Payment	29	view_payment
117	Can add payment attempt	30	add_paymentattempt
118	Can change payment attempt	30	change_paymentattempt
119	Can delete payment attempt	30	delete_paymentattempt
120	Can view payment attempt	30	view_paymentattempt
121	Can add refund transaction	31	add_refundtransaction
122	Can change refund transaction	31	change_refundtransaction
123	Can delete refund transaction	31	delete_refundtransaction
124	Can view refund transaction	31	view_refundtransaction
125	Can add Coupon	32	add_coupon
126	Can change Coupon	32	change_coupon
127	Can delete Coupon	32	delete_coupon
128	Can view Coupon	32	view_coupon
129	Can add Coupon Redemption	33	add_couponredemption
130	Can change Coupon Redemption	33	change_couponredemption
131	Can delete Coupon Redemption	33	delete_couponredemption
132	Can view Coupon Redemption	33	view_couponredemption
133	Can add Banner	34	add_banner
134	Can change Banner	34	change_banner
135	Can delete Banner	34	delete_banner
136	Can view Banner	34	view_banner
137	Can add Newsletter Subscription	35	add_newslettersubscription
138	Can change Newsletter Subscription	35	change_newslettersubscription
139	Can delete Newsletter Subscription	35	delete_newslettersubscription
140	Can view Newsletter Subscription	35	view_newslettersubscription
141	Can add Page	36	add_page
142	Can change Page	36	change_page
143	Can delete Page	36	delete_page
144	Can view Page	36	view_page
145	Can add Site Setting	37	add_sitesetting
146	Can change Site Setting	37	change_sitesetting
147	Can delete Site Setting	37	delete_sitesetting
148	Can view Site Setting	37	view_sitesetting
\.


--
-- Data for Name: cart_cart; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.cart_cart (created_at, updated_at, id, session_key, user_id) FROM stdin;
2026-10-25 23:09:50.854182+05:30	2026-10-25 23:09:50.854213+05:30	64154396-a25b-4a0b-8913-e7678bf7d26d	dwsnxfool07bedxxn4v9ky3wwm8nms81	\N
2026-10-25 23:12:21.873284+05:30	2026-10-25 23:12:21.873317+05:30	6de1ec3e-76fb-4cdb-a44c-9975e8fd24db	lz5ajz1uqi93h027a7b81rr0aloby3ag	\N
2026-10-25 23:14:06.934609+05:30	2026-10-25 23:14:06.934616+05:30	696e6663-c963-4c88-a8ce-48fa68999a2b	olmg0g0i7sicz8adkqxkj5b97ibabh9t	\N
2026-10-25 23:26:34.243363+05:30	2026-10-25 23:26:34.243374+05:30	4b93a577-8e28-40d5-97ef-9d8d1ec9b813	\N	ecd7b997-806a-418b-854b-5943e5a95f92
\.


--
-- Data for Name: cart_cartitem; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.cart_cartitem (created_at, updated_at, id, quantity, cart_id, product_id, variant_id) FROM stdin;
\.


--
-- Data for Name: cart_wishlist; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.cart_wishlist (created_at, updated_at, id, user_id) FROM stdin;
\.


--
-- Data for Name: cart_wishlistitem; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.cart_wishlistitem (created_at, updated_at, id, product_id, wishlist_id) FROM stdin;
\.


--
-- Data for Name: catalog_category; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.catalog_category (created_at, updated_at, id, name, slug, description, image, is_featured, is_active, sort_order, parent_id) FROM stdin;
2026-10-25 22:14:09.131736+05:30	2026-10-25 22:14:09.13175+05:30	a9cb5c75-fa8f-4df1-bf0a-f2e08909e6ee	Apparel & Linens	apparel-linens	Unstructured silhouettes crafted from raw organic linen and unbleached cotton.		t	t	1	\N
2026-10-25 22:14:09.135403+05:30	2026-10-25 22:14:09.13541+05:30	5ba33302-ad8f-4291-a2d0-0a1ea4a5e8b9	Sculptural Ceramics	sculptural-ceramics	Wheel-thrown and hand-glazed vessels with tactile matte finishes.		t	t	2	\N
2026-10-25 22:14:09.136361+05:30	2026-10-25 22:14:09.136367+05:30	a51718b1-7d4a-44a9-a5ec-5f5e2f056fa8	Living & Objects	living-objects	Handcrafted accents designed to harmonize residential sanctuaries.		t	t	3	\N
2026-10-25 22:14:09.137188+05:30	2026-10-25 22:14:09.137193+05:30	0ba48fc3-311f-4dc2-bc79-761bf381b759	Ambient Lighting	ambient-lighting	Warm muted illumination forged in raw brass, stone, and washi paper.		t	t	4	\N
\.


--
-- Data for Name: catalog_product; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.catalog_product (created_at, updated_at, id, name, slug, sku, short_description, description, price, compare_at_price, cost_price, is_featured, is_trending, is_new_arrival, is_active, is_archived, tags, category_id) FROM stdin;
2026-10-25 22:14:09.144785+05:30	2026-10-25 22:14:09.144794+05:30	acc23960-1494-46f7-9acd-38555bfbe78f	Raw Linen Kimono Robe	raw-linen-kimono-robe	ZY-APP-001	Relaxed dropped-shoulder lounge robe woven from heavy European flax.	Crafted from 100% pre-washed European flax linen, this robe combines effortless lounge elegance with breathability. Features deep patch pockets, a matching tie belt, and self-finished seams for daily ritual comfort.	3450.00	4200.00	\N	t	t	f	t	f		a9cb5c75-fa8f-4df1-bf0a-f2e08909e6ee
2026-10-25 22:14:09.15224+05:30	2026-10-25 22:14:09.152246+05:30	d7bd82e1-fb5d-4719-8e41-b4554de50cb4	Hand-Thrown Stoneware Vessel	hand-thrown-stoneware-vessel	ZY-CER-002	Sculptural unglazed vase with tactile sand-textured slip.	Each vessel is wheel-thrown individually by master ceramicists using natural stoneware clay. Left raw on the exterior to preserve natural earth texture, the interior is glazed water-tight for fresh botanicals.	2100.00	2500.00	\N	t	t	t	t	f		5ba33302-ad8f-4291-a2d0-0a1ea4a5e8b9
2026-10-25 22:14:09.154103+05:30	2026-10-25 22:14:09.154108+05:30	2223ece5-7c0a-4201-84fd-f678e616d7d4	Oatmeal Ceramic Tasting Cup	oatmeal-ceramic-tasting-cup	ZY-CER-003	Ergonomic handle-free ceramic cup for pour-overs and matcha.	Formed to nestle naturally into palm hands, this tasting cup features an oatmeal satin glaze with delicate speckles. Dishwasher and microwave safe.	850.00	\N	\N	f	t	f	t	f		5ba33302-ad8f-4291-a2d0-0a1ea4a5e8b9
2026-10-25 22:14:09.155979+05:30	2026-10-25 22:14:09.155984+05:30	92679243-6d5e-40df-b3bc-31cf98b470da	Sandalwood & Vetiver Botanical Candle	sandalwood-vetiver-botanical-candle	ZY-OBJ-004	Hand-poured coconut-soy wax in a reusable matte ceramic pot.	Earthy Mysore sandalwood infused with smoky Haitian vetiver and warm cedar. 55 hours of clean burning time with an unbleached cotton wick.	1250.00	1500.00	\N	t	f	t	t	f		a51718b1-7d4a-44a9-a5ec-5f5e2f056fa8
2026-10-25 22:14:09.157771+05:30	2026-10-25 22:14:09.157776+05:30	d09f14d5-de34-4381-b76d-75ce6a7e513a	Woven Jute & Wool Textured Throw	woven-jute-wool-textured-throw	ZY-APP-005	Heavyweight tactile blanket finished with delicate raw fringe.	An artisanal blend of undyed sheep wool and natural jute yarn, woven on traditional shuttle looms. Delivers warm tactile comfort for winter evenings.	4800.00	5600.00	\N	t	t	f	t	f		a9cb5c75-fa8f-4df1-bf0a-f2e08909e6ee
2026-10-25 22:14:09.159889+05:30	2026-10-25 22:14:09.159896+05:30	ca2d067c-82a9-463d-94cf-b1b345f49bbb	Brushed Brass Minimalist Desk Lamp	brushed-brass-minimalist-desk-lamp	ZY-LGT-006	Solid brass architectural reading lamp with diffused warm LED.	A study in elemental geometric forms. Hand-brushed raw brass that patinas gracefully over years. Features integrated touch dimming and warm 2700K ambient light.	6200.00	\N	\N	t	f	t	t	f		0ba48fc3-311f-4dc2-bc79-761bf381b759
\.


--
-- Data for Name: catalog_productattribute; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.catalog_productattribute (id, created_at, updated_at, name, slug) FROM stdin;
\.


--
-- Data for Name: catalog_productimage; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.catalog_productimage (created_at, updated_at, id, image, alt_text, is_feature, sort_order, product_id) FROM stdin;
\.


--
-- Data for Name: catalog_productreview; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.catalog_productreview (created_at, updated_at, id, rating, title, comment, is_approved, product_id, user_id) FROM stdin;
\.


--
-- Data for Name: catalog_productvariant; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.catalog_productvariant (created_at, updated_at, id, name, sku, price_override, attributes, is_active, product_id) FROM stdin;
\.


--
-- Data for Name: content_banner; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.content_banner (created_at, updated_at, id, title, subtitle, image, link_url, button_text, location, is_active, sort_order) FROM stdin;
\.


--
-- Data for Name: content_newslettersubscription; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.content_newslettersubscription (id, created_at, updated_at, email, is_active) FROM stdin;
\.


--
-- Data for Name: content_page; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.content_page (created_at, updated_at, id, title, slug, content, meta_description, is_published) FROM stdin;
2026-10-25 22:14:09.169409+05:30	2026-10-25 22:14:09.169414+05:30	b01713d6-d15f-47a1-af5a-9c27ca28de7b	About Ziyo	about-us	Founded on the principles of quiet luxury and conscious materiality, Ziyo curates living objects that speak through texture, form, and honesty. We reject disposable trends in favor of timeless silhouettes handcrafted by generational artisans across India and Japan.\n\nOur products are made from renewable natural fibers, unglazed stoneware, and solid metals that age gracefully alongside the stories of your home.	Discover the story and material philosophy behind Ziyo's curated essentials.	t
2026-10-25 22:14:09.170739+05:30	2026-10-25 22:14:09.170744+05:30	c9d8c591-2472-475e-aff6-bfcc07e9d7a1	Shipping & Delivery Policy	shipping-policy	All orders are processed and carefully packaged within 24 to 48 business hours from our central fulfillment studio.\n\nStandard express domestic delivery takes 2 to 4 business days. Orders over ₹1,499 receive complimentary express shipping. For orders below ₹1,499, a flat delivery fee of ₹99 applies nationwide.\n\nReal-time tracking links are transmitted via email as soon as packages are transferred to our carrier partners.	Transparent domestic express shipping policies for all Ziyo orders.	t
2026-10-25 22:14:09.171495+05:30	2026-10-25 22:14:09.1715+05:30	f46ba4c7-d87d-419f-83b9-a4ade964a02e	Returns & Refunds Policy	returns-refunds	We invite you to experience our objects with complete peace of mind. We gladly accept returns for unused, unworn items in original packaging within 14 days of receipt.\n\nTo initiate a return, navigate to your order history and select 'Request Return', or contact concierge@ziyo.store. Once inspected at our studio, refunds are credited back to your original payment method within 5 to 7 business days.	Our 14-day hassle-free return and refund policy.	t
\.


--
-- Data for Name: content_sitesetting; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.content_sitesetting (id, created_at, updated_at, key, value, description) FROM stdin;
1	2026-10-25 22:14:09.174+05:30	2026-10-25 23:26:55.811174+05:30	STORE_NAME	Ziyo	Store branding name
2	2026-10-25 22:14:09.175357+05:30	2026-10-25 23:26:55.812822+05:30	STORE_EMAIL		Primary support email
3	2026-10-25 22:14:09.176168+05:30	2026-10-25 23:26:55.814484+05:30	STORE_PHONE		Customer care hotline
4	2026-10-25 22:14:09.177441+05:30	2026-10-25 23:26:55.815917+05:30	STORE_TAGLINE		Brand slogan
\.


--
-- Data for Name: core_auditlog; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.core_auditlog (id, user_email, action, resource_type, resource_id, ip_address, user_agent, details, "timestamp", user_id) FROM stdin;
b827dc03-026a-4623-ba1f-750993585edb	ziyo@example.com	UPDATE	Admin Path: /login/		127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36 Edg/156.0.0.0	{"method": "POST", "status_code": 302}	2026-10-25 23:26:34.220135+05:30	ecd7b997-806a-418b-854b-5943e5a95f92
7a62d96b-026e-4008-9105-ba9e808648ae	ziyo@example.com	UPDATE	Admin Path: /settings/		127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36 Edg/156.0.0.0	{"method": "POST", "status_code": 302}	2026-10-25 23:26:55.81686+05:30	ecd7b997-806a-418b-854b-5943e5a95f92
\.


--
-- Data for Name: discounts_coupon; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.discounts_coupon (created_at, updated_at, id, code, discount_type, value, min_purchase_amount, max_discount_amount, usage_limit, per_user_limit, used_count, valid_from, valid_to, is_active) FROM stdin;
2026-10-25 22:14:09.164657+05:30	2026-10-25 22:14:09.164665+05:30	c78aa731-935b-4b69-b7db-a59e061b77ba	ZIYO10	PERCENTAGE	10.00	1000.00	\N	\N	1	0	2026-10-25 22:14:09.161601+05:30	2027-10-25 22:14:09.161601+05:30	t
2026-10-25 22:14:09.166298+05:30	2026-10-25 22:14:09.166304+05:30	99e42706-3ed0-4d82-81e4-8c6112e0b1c2	WELCOME200	FIXED_AMOUNT	200.00	1200.00	\N	\N	1	0	2026-10-25 22:14:09.161601+05:30	2027-10-25 22:14:09.161601+05:30	t
\.


--
-- Data for Name: discounts_couponredemption; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.discounts_couponredemption (created_at, updated_at, id, order_id, discount_amount, coupon_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	core	auditlog
7	accounts	user
8	accounts	customeraddress
9	accounts	userprofile
10	catalog	productattribute
11	catalog	category
12	catalog	product
13	catalog	productimage
14	catalog	productvariant
15	catalog	productreview
16	inventory	inventoryitem
17	inventory	stockmovement
18	inventory	stockreservation
19	cart	cart
20	cart	wishlist
21	cart	cartitem
22	cart	wishlistitem
23	orders	order
24	orders	orderitem
25	orders	orderstatushistory
26	orders	returnrequest
27	orders	shipment
28	payments	paymentwebhookevent
29	payments	payment
30	payments	paymentattempt
31	payments	refundtransaction
32	discounts	coupon
33	discounts	couponredemption
34	content	banner
35	content	newslettersubscription
36	content	page
37	content	sitesetting
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-10-25 22:13:58.956416+05:30
2	contenttypes	0002_remove_content_type_name	2026-10-25 22:13:58.960932+05:30
3	auth	0001_initial	2026-10-25 22:13:58.995367+05:30
4	auth	0002_alter_permission_name_max_length	2026-10-25 22:13:58.998412+05:30
5	auth	0003_alter_user_email_max_length	2026-10-25 22:13:59.001396+05:30
6	auth	0004_alter_user_username_opts	2026-10-25 22:13:59.003807+05:30
7	auth	0005_alter_user_last_login_null	2026-10-25 22:13:59.006167+05:30
8	auth	0006_require_contenttypes_0002	2026-10-25 22:13:59.006812+05:30
9	auth	0007_alter_validators_add_error_messages	2026-10-25 22:13:59.009707+05:30
10	auth	0008_alter_user_username_max_length	2026-10-25 22:13:59.01233+05:30
11	auth	0009_alter_user_last_name_max_length	2026-10-25 22:13:59.014841+05:30
12	auth	0010_alter_group_name_max_length	2026-10-25 22:13:59.018629+05:30
13	auth	0011_update_proxy_permissions	2026-10-25 22:13:59.021351+05:30
14	auth	0012_alter_user_first_name_max_length	2026-10-25 22:13:59.024022+05:30
15	accounts	0001_initial	2026-10-25 22:13:59.093404+05:30
16	admin	0001_initial	2026-10-25 22:13:59.111015+05:30
17	admin	0002_logentry_remove_auto_add	2026-10-25 22:13:59.116406+05:30
18	admin	0003_logentry_add_action_flag_choices	2026-10-25 22:13:59.121676+05:30
19	catalog	0001_initial	2026-10-25 22:13:59.227108+05:30
20	cart	0001_initial	2026-10-25 22:13:59.309714+05:30
21	content	0001_initial	2026-10-25 22:13:59.346962+05:30
22	core	0001_initial	2026-10-25 22:13:59.371696+05:30
23	discounts	0001_initial	2026-10-25 22:13:59.407459+05:30
24	inventory	0001_initial	2026-10-25 22:13:59.473464+05:30
25	orders	0001_initial	2026-10-25 22:13:59.60197+05:30
26	payments	0001_initial	2026-10-25 22:13:59.702625+05:30
27	sessions	0001_initial	2026-10-25 22:13:59.711202+05:30
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
olmg0g0i7sicz8adkqxkj5b97ibabh9t	e30:1xL2GM:ZAYvHAHPoTg70z9sZEJAwe4I4paflb07YUUspmIZ3eQ	2026-11-08 23:14:06.980073+05:30
tjuswh3tirjfzc2o05hemv0sbz4nudsk	.eJxVjDkOwkAMRe8yNRmFWWKbkp4zRPbYISxKpCwV4u4QKQWUX--9_3Itr0vfrrNN7U3dyVlRECKosG64SkeUCnOSKlOKlplyR8EdfjPh8rBha_XOw3X0ZRyW6SZ-U_xOZ38Z1Z7n3f076Hnut1pUiVkDJpEEwgT5u43UDENTUil17ow6yLFAzNwQKnIASjVCjO79AQo3QYQ:1xL2SQ:fdr5sgL-Hc9Uu4F8nab4_1oGHkSflNlmB9sYitGx0s0	2026-11-08 23:26:34.22661+05:30
\.


--
-- Data for Name: inventory_inventoryitem; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.inventory_inventoryitem (created_at, updated_at, id, sku, quantity_on_hand, reserved_quantity, low_stock_threshold, product_id, variant_id) FROM stdin;
2026-10-25 22:14:09.150559+05:30	2026-10-25 22:14:09.150567+05:30	c88f27a7-8b30-4f97-9296-14e12ac421e8	ZY-APP-001	45	0	5	acc23960-1494-46f7-9acd-38555bfbe78f	\N
2026-10-25 22:14:09.153183+05:30	2026-10-25 22:14:09.153188+05:30	845b7732-c5bc-46ed-9d3f-b98aa191e1b0	ZY-CER-002	25	0	5	d7bd82e1-fb5d-4719-8e41-b4554de50cb4	\N
2026-10-25 22:14:09.155001+05:30	2026-10-25 22:14:09.155006+05:30	587ba3e6-70ab-4e54-9957-887027f1425a	ZY-CER-003	60	0	5	2223ece5-7c0a-4201-84fd-f678e616d7d4	\N
2026-10-25 22:14:09.156863+05:30	2026-10-25 22:14:09.156868+05:30	61670e50-fbcf-4a80-9803-25b1d040f756	ZY-OBJ-004	40	0	5	92679243-6d5e-40df-b3bc-31cf98b470da	\N
2026-10-25 22:14:09.158633+05:30	2026-10-25 22:14:09.158638+05:30	94a6d883-ee04-4c14-99f9-166ba94c92f8	ZY-APP-005	18	0	5	d09f14d5-de34-4381-b76d-75ce6a7e513a	\N
2026-10-25 22:14:09.16111+05:30	2026-10-25 22:14:09.161116+05:30	8240b1ca-ff21-46b6-bb4e-0c0a50d07bad	ZY-LGT-006	12	0	5	ca2d067c-82a9-463d-94cf-b1b345f49bbb	\N
\.


--
-- Data for Name: inventory_stockmovement; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.inventory_stockmovement (created_at, updated_at, id, movement_type, quantity, reference_id, notes, inventory_item_id, user_id) FROM stdin;
\.


--
-- Data for Name: inventory_stockreservation; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.inventory_stockreservation (created_at, updated_at, id, quantity, reference_id, is_released, inventory_item_id) FROM stdin;
\.


--
-- Data for Name: orders_order; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.orders_order (created_at, updated_at, id, order_number, email, phone, status, subtotal, discount_amount, coupon_code, shipping_fee, tax_amount, total_amount, shipping_full_name, shipping_phone, shipping_address_line_1, shipping_address_line_2, shipping_city, shipping_state, shipping_postal_code, shipping_country, customer_notes, admin_notes, tracking_number, carrier, user_id) FROM stdin;
\.


--
-- Data for Name: orders_orderitem; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.orders_orderitem (created_at, updated_at, id, product_name, variant_name, sku, unit_price, quantity, line_total, order_id, product_id) FROM stdin;
\.


--
-- Data for Name: orders_orderstatushistory; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.orders_orderstatushistory (created_at, updated_at, id, status, notes, changed_by_id, order_id) FROM stdin;
\.


--
-- Data for Name: orders_returnrequest; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.orders_returnrequest (created_at, updated_at, id, reason, status, admin_notes, order_id, user_id) FROM stdin;
\.


--
-- Data for Name: orders_shipment; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.orders_shipment (created_at, updated_at, id, carrier, tracking_number, shipped_at, estimated_delivery, order_id) FROM stdin;
\.


--
-- Data for Name: payments_payment; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.payments_payment (created_at, updated_at, id, provider, transaction_id, gateway_order_id, amount, currency, status, payment_method_type, raw_response, order_id) FROM stdin;
\.


--
-- Data for Name: payments_paymentattempt; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.payments_paymentattempt (created_at, updated_at, id, gateway_order_id, status, error_code, error_description, order_id) FROM stdin;
\.


--
-- Data for Name: payments_paymentwebhookevent; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.payments_paymentwebhookevent (created_at, updated_at, id, event_id, event_type, provider, payload, is_processed, processed_at) FROM stdin;
\.


--
-- Data for Name: payments_refundtransaction; Type: TABLE DATA; Schema: public; Owner: ZIYO
--

COPY public.payments_refundtransaction (created_at, updated_at, id, refund_id, amount, reason, status, initiated_by_id, payment_id) FROM stdin;
\.


--
-- Name: accounts_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ZIYO
--

SELECT pg_catalog.setval('public.accounts_user_groups_id_seq', 1, false);


--
-- Name: accounts_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ZIYO
--

SELECT pg_catalog.setval('public.accounts_user_user_permissions_id_seq', 1, false);


--
-- Name: accounts_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ZIYO
--

SELECT pg_catalog.setval('public.accounts_userprofile_id_seq', 2, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ZIYO
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ZIYO
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ZIYO
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 148, true);


--
-- Name: catalog_productattribute_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ZIYO
--

SELECT pg_catalog.setval('public.catalog_productattribute_id_seq', 1, false);


--
-- Name: content_newslettersubscription_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ZIYO
--

SELECT pg_catalog.setval('public.content_newslettersubscription_id_seq', 1, false);


--
-- Name: content_sitesetting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ZIYO
--

SELECT pg_catalog.setval('public.content_sitesetting_id_seq', 4, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ZIYO
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ZIYO
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 37, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ZIYO
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 27, true);


--
-- Name: accounts_customeraddress accounts_customeraddress_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_customeraddress
    ADD CONSTRAINT accounts_customeraddress_pkey PRIMARY KEY (id);


--
-- Name: accounts_user accounts_user_email_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_user
    ADD CONSTRAINT accounts_user_email_key UNIQUE (email);


--
-- Name: accounts_user_groups accounts_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_user_groups
    ADD CONSTRAINT accounts_user_groups_pkey PRIMARY KEY (id);


--
-- Name: accounts_user_groups accounts_user_groups_user_id_group_id_59c0b32f_uniq; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_user_groups
    ADD CONSTRAINT accounts_user_groups_user_id_group_id_59c0b32f_uniq UNIQUE (user_id, group_id);


--
-- Name: accounts_user accounts_user_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_user
    ADD CONSTRAINT accounts_user_pkey PRIMARY KEY (id);


--
-- Name: accounts_user_user_permissions accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_user_user_permissions
    ADD CONSTRAINT accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq UNIQUE (user_id, permission_id);


--
-- Name: accounts_user_user_permissions accounts_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_user_user_permissions
    ADD CONSTRAINT accounts_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: accounts_userprofile accounts_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_pkey PRIMARY KEY (id);


--
-- Name: accounts_userprofile accounts_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: cart_cart cart_cart_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_cart
    ADD CONSTRAINT cart_cart_pkey PRIMARY KEY (id);


--
-- Name: cart_cartitem cart_cartitem_cart_id_product_id_variant_id_5fc0c5f3_uniq; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_cartitem
    ADD CONSTRAINT cart_cartitem_cart_id_product_id_variant_id_5fc0c5f3_uniq UNIQUE (cart_id, product_id, variant_id);


--
-- Name: cart_cartitem cart_cartitem_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_cartitem
    ADD CONSTRAINT cart_cartitem_pkey PRIMARY KEY (id);


--
-- Name: cart_wishlist cart_wishlist_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_wishlist
    ADD CONSTRAINT cart_wishlist_pkey PRIMARY KEY (id);


--
-- Name: cart_wishlist cart_wishlist_user_id_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_wishlist
    ADD CONSTRAINT cart_wishlist_user_id_key UNIQUE (user_id);


--
-- Name: cart_wishlistitem cart_wishlistitem_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_wishlistitem
    ADD CONSTRAINT cart_wishlistitem_pkey PRIMARY KEY (id);


--
-- Name: cart_wishlistitem cart_wishlistitem_wishlist_id_product_id_ec03f6f6_uniq; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_wishlistitem
    ADD CONSTRAINT cart_wishlistitem_wishlist_id_product_id_ec03f6f6_uniq UNIQUE (wishlist_id, product_id);


--
-- Name: catalog_category catalog_category_name_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_category
    ADD CONSTRAINT catalog_category_name_key UNIQUE (name);


--
-- Name: catalog_category catalog_category_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_category
    ADD CONSTRAINT catalog_category_pkey PRIMARY KEY (id);


--
-- Name: catalog_category catalog_category_slug_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_category
    ADD CONSTRAINT catalog_category_slug_key UNIQUE (slug);


--
-- Name: catalog_product catalog_product_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_product
    ADD CONSTRAINT catalog_product_pkey PRIMARY KEY (id);


--
-- Name: catalog_product catalog_product_sku_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_product
    ADD CONSTRAINT catalog_product_sku_key UNIQUE (sku);


--
-- Name: catalog_product catalog_product_slug_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_product
    ADD CONSTRAINT catalog_product_slug_key UNIQUE (slug);


--
-- Name: catalog_productattribute catalog_productattribute_name_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_productattribute
    ADD CONSTRAINT catalog_productattribute_name_key UNIQUE (name);


--
-- Name: catalog_productattribute catalog_productattribute_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_productattribute
    ADD CONSTRAINT catalog_productattribute_pkey PRIMARY KEY (id);


--
-- Name: catalog_productattribute catalog_productattribute_slug_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_productattribute
    ADD CONSTRAINT catalog_productattribute_slug_key UNIQUE (slug);


--
-- Name: catalog_productimage catalog_productimage_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_productimage
    ADD CONSTRAINT catalog_productimage_pkey PRIMARY KEY (id);


--
-- Name: catalog_productreview catalog_productreview_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_productreview
    ADD CONSTRAINT catalog_productreview_pkey PRIMARY KEY (id);


--
-- Name: catalog_productreview catalog_productreview_product_id_user_id_4c0fbc41_uniq; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_productreview
    ADD CONSTRAINT catalog_productreview_product_id_user_id_4c0fbc41_uniq UNIQUE (product_id, user_id);


--
-- Name: catalog_productvariant catalog_productvariant_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_productvariant
    ADD CONSTRAINT catalog_productvariant_pkey PRIMARY KEY (id);


--
-- Name: catalog_productvariant catalog_productvariant_sku_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_productvariant
    ADD CONSTRAINT catalog_productvariant_sku_key UNIQUE (sku);


--
-- Name: content_banner content_banner_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.content_banner
    ADD CONSTRAINT content_banner_pkey PRIMARY KEY (id);


--
-- Name: content_newslettersubscription content_newslettersubscription_email_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.content_newslettersubscription
    ADD CONSTRAINT content_newslettersubscription_email_key UNIQUE (email);


--
-- Name: content_newslettersubscription content_newslettersubscription_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.content_newslettersubscription
    ADD CONSTRAINT content_newslettersubscription_pkey PRIMARY KEY (id);


--
-- Name: content_page content_page_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.content_page
    ADD CONSTRAINT content_page_pkey PRIMARY KEY (id);


--
-- Name: content_page content_page_slug_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.content_page
    ADD CONSTRAINT content_page_slug_key UNIQUE (slug);


--
-- Name: content_sitesetting content_sitesetting_key_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.content_sitesetting
    ADD CONSTRAINT content_sitesetting_key_key UNIQUE (key);


--
-- Name: content_sitesetting content_sitesetting_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.content_sitesetting
    ADD CONSTRAINT content_sitesetting_pkey PRIMARY KEY (id);


--
-- Name: core_auditlog core_auditlog_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.core_auditlog
    ADD CONSTRAINT core_auditlog_pkey PRIMARY KEY (id);


--
-- Name: discounts_coupon discounts_coupon_code_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.discounts_coupon
    ADD CONSTRAINT discounts_coupon_code_key UNIQUE (code);


--
-- Name: discounts_coupon discounts_coupon_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.discounts_coupon
    ADD CONSTRAINT discounts_coupon_pkey PRIMARY KEY (id);


--
-- Name: discounts_couponredemption discounts_couponredemption_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.discounts_couponredemption
    ADD CONSTRAINT discounts_couponredemption_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: inventory_inventoryitem inventory_inventoryitem_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.inventory_inventoryitem
    ADD CONSTRAINT inventory_inventoryitem_pkey PRIMARY KEY (id);


--
-- Name: inventory_inventoryitem inventory_inventoryitem_product_id_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.inventory_inventoryitem
    ADD CONSTRAINT inventory_inventoryitem_product_id_key UNIQUE (product_id);


--
-- Name: inventory_inventoryitem inventory_inventoryitem_sku_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.inventory_inventoryitem
    ADD CONSTRAINT inventory_inventoryitem_sku_key UNIQUE (sku);


--
-- Name: inventory_inventoryitem inventory_inventoryitem_variant_id_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.inventory_inventoryitem
    ADD CONSTRAINT inventory_inventoryitem_variant_id_key UNIQUE (variant_id);


--
-- Name: inventory_stockmovement inventory_stockmovement_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.inventory_stockmovement
    ADD CONSTRAINT inventory_stockmovement_pkey PRIMARY KEY (id);


--
-- Name: inventory_stockreservation inventory_stockreservation_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.inventory_stockreservation
    ADD CONSTRAINT inventory_stockreservation_pkey PRIMARY KEY (id);


--
-- Name: orders_order orders_order_order_number_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_order_number_key UNIQUE (order_number);


--
-- Name: orders_order orders_order_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_pkey PRIMARY KEY (id);


--
-- Name: orders_orderitem orders_orderitem_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_orderitem
    ADD CONSTRAINT orders_orderitem_pkey PRIMARY KEY (id);


--
-- Name: orders_orderstatushistory orders_orderstatushistory_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_orderstatushistory
    ADD CONSTRAINT orders_orderstatushistory_pkey PRIMARY KEY (id);


--
-- Name: orders_returnrequest orders_returnrequest_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_returnrequest
    ADD CONSTRAINT orders_returnrequest_pkey PRIMARY KEY (id);


--
-- Name: orders_shipment orders_shipment_order_id_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_shipment
    ADD CONSTRAINT orders_shipment_order_id_key UNIQUE (order_id);


--
-- Name: orders_shipment orders_shipment_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_shipment
    ADD CONSTRAINT orders_shipment_pkey PRIMARY KEY (id);


--
-- Name: payments_payment payments_payment_order_id_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.payments_payment
    ADD CONSTRAINT payments_payment_order_id_key UNIQUE (order_id);


--
-- Name: payments_payment payments_payment_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.payments_payment
    ADD CONSTRAINT payments_payment_pkey PRIMARY KEY (id);


--
-- Name: payments_payment payments_payment_transaction_id_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.payments_payment
    ADD CONSTRAINT payments_payment_transaction_id_key UNIQUE (transaction_id);


--
-- Name: payments_paymentattempt payments_paymentattempt_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.payments_paymentattempt
    ADD CONSTRAINT payments_paymentattempt_pkey PRIMARY KEY (id);


--
-- Name: payments_paymentwebhookevent payments_paymentwebhookevent_event_id_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.payments_paymentwebhookevent
    ADD CONSTRAINT payments_paymentwebhookevent_event_id_key UNIQUE (event_id);


--
-- Name: payments_paymentwebhookevent payments_paymentwebhookevent_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.payments_paymentwebhookevent
    ADD CONSTRAINT payments_paymentwebhookevent_pkey PRIMARY KEY (id);


--
-- Name: payments_refundtransaction payments_refundtransaction_pkey; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.payments_refundtransaction
    ADD CONSTRAINT payments_refundtransaction_pkey PRIMARY KEY (id);


--
-- Name: payments_refundtransaction payments_refundtransaction_refund_id_key; Type: CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.payments_refundtransaction
    ADD CONSTRAINT payments_refundtransaction_refund_id_key UNIQUE (refund_id);


--
-- Name: accounts_customeraddress_created_at_84b947d5; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX accounts_customeraddress_created_at_84b947d5 ON public.accounts_customeraddress USING btree (created_at);


--
-- Name: accounts_customeraddress_user_id_09d750f6; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX accounts_customeraddress_user_id_09d750f6 ON public.accounts_customeraddress USING btree (user_id);


--
-- Name: accounts_user_email_b2644a56_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX accounts_user_email_b2644a56_like ON public.accounts_user USING btree (email varchar_pattern_ops);


--
-- Name: accounts_user_groups_group_id_bd11a704; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX accounts_user_groups_group_id_bd11a704 ON public.accounts_user_groups USING btree (group_id);


--
-- Name: accounts_user_groups_user_id_52b62117; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX accounts_user_groups_user_id_52b62117 ON public.accounts_user_groups USING btree (user_id);


--
-- Name: accounts_user_role_57e97df0; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX accounts_user_role_57e97df0 ON public.accounts_user USING btree (role);


--
-- Name: accounts_user_role_57e97df0_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX accounts_user_role_57e97df0_like ON public.accounts_user USING btree (role varchar_pattern_ops);


--
-- Name: accounts_user_user_permissions_permission_id_113bb443; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX accounts_user_user_permissions_permission_id_113bb443 ON public.accounts_user_user_permissions USING btree (permission_id);


--
-- Name: accounts_user_user_permissions_user_id_e4f0a161; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX accounts_user_user_permissions_user_id_e4f0a161 ON public.accounts_user_user_permissions USING btree (user_id);


--
-- Name: accounts_userprofile_created_at_0f764602; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX accounts_userprofile_created_at_0f764602 ON public.accounts_userprofile USING btree (created_at);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: cart_cart_created_at_82800f17; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX cart_cart_created_at_82800f17 ON public.cart_cart USING btree (created_at);


--
-- Name: cart_cart_session_key_bf21cb35; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX cart_cart_session_key_bf21cb35 ON public.cart_cart USING btree (session_key);


--
-- Name: cart_cart_session_key_bf21cb35_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX cart_cart_session_key_bf21cb35_like ON public.cart_cart USING btree (session_key varchar_pattern_ops);


--
-- Name: cart_cart_user_id_9b4220b9; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX cart_cart_user_id_9b4220b9 ON public.cart_cart USING btree (user_id);


--
-- Name: cart_cartitem_cart_id_370ad265; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX cart_cartitem_cart_id_370ad265 ON public.cart_cartitem USING btree (cart_id);


--
-- Name: cart_cartitem_created_at_f0361bf9; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX cart_cartitem_created_at_f0361bf9 ON public.cart_cartitem USING btree (created_at);


--
-- Name: cart_cartitem_product_id_b24e265a; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX cart_cartitem_product_id_b24e265a ON public.cart_cartitem USING btree (product_id);


--
-- Name: cart_cartitem_variant_id_69f5d8c8; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX cart_cartitem_variant_id_69f5d8c8 ON public.cart_cartitem USING btree (variant_id);


--
-- Name: cart_wishlist_created_at_87ebfab4; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX cart_wishlist_created_at_87ebfab4 ON public.cart_wishlist USING btree (created_at);


--
-- Name: cart_wishlistitem_created_at_0a951113; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX cart_wishlistitem_created_at_0a951113 ON public.cart_wishlistitem USING btree (created_at);


--
-- Name: cart_wishlistitem_product_id_c183b0d4; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX cart_wishlistitem_product_id_c183b0d4 ON public.cart_wishlistitem USING btree (product_id);


--
-- Name: cart_wishlistitem_wishlist_id_dd2c2649; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX cart_wishlistitem_wishlist_id_dd2c2649 ON public.cart_wishlistitem USING btree (wishlist_id);


--
-- Name: catalog_category_created_at_2f95ea55; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_category_created_at_2f95ea55 ON public.catalog_category USING btree (created_at);


--
-- Name: catalog_category_is_active_66b33fbf; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_category_is_active_66b33fbf ON public.catalog_category USING btree (is_active);


--
-- Name: catalog_category_is_featured_efab636a; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_category_is_featured_efab636a ON public.catalog_category USING btree (is_featured);


--
-- Name: catalog_category_name_fdc3466c_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_category_name_fdc3466c_like ON public.catalog_category USING btree (name varchar_pattern_ops);


--
-- Name: catalog_category_parent_id_f61bd017; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_category_parent_id_f61bd017 ON public.catalog_category USING btree (parent_id);


--
-- Name: catalog_category_slug_dbf63ad0_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_category_slug_dbf63ad0_like ON public.catalog_category USING btree (slug varchar_pattern_ops);


--
-- Name: catalog_product_category_id_35bf920b; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_product_category_id_35bf920b ON public.catalog_product USING btree (category_id);


--
-- Name: catalog_product_created_at_ea90ae72; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_product_created_at_ea90ae72 ON public.catalog_product USING btree (created_at);


--
-- Name: catalog_product_is_active_6ce66e03; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_product_is_active_6ce66e03 ON public.catalog_product USING btree (is_active);


--
-- Name: catalog_product_is_archived_cd365c0e; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_product_is_archived_cd365c0e ON public.catalog_product USING btree (is_archived);


--
-- Name: catalog_product_is_featured_4286e684; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_product_is_featured_4286e684 ON public.catalog_product USING btree (is_featured);


--
-- Name: catalog_product_is_new_arrival_eef7e0fb; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_product_is_new_arrival_eef7e0fb ON public.catalog_product USING btree (is_new_arrival);


--
-- Name: catalog_product_is_trending_33a3a09e; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_product_is_trending_33a3a09e ON public.catalog_product USING btree (is_trending);


--
-- Name: catalog_product_name_924af5bc; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_product_name_924af5bc ON public.catalog_product USING btree (name);


--
-- Name: catalog_product_name_924af5bc_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_product_name_924af5bc_like ON public.catalog_product USING btree (name varchar_pattern_ops);


--
-- Name: catalog_product_price_1347cb30; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_product_price_1347cb30 ON public.catalog_product USING btree (price);


--
-- Name: catalog_product_sku_5c54c070_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_product_sku_5c54c070_like ON public.catalog_product USING btree (sku varchar_pattern_ops);


--
-- Name: catalog_product_slug_f37848b0_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_product_slug_f37848b0_like ON public.catalog_product USING btree (slug varchar_pattern_ops);


--
-- Name: catalog_productattribute_created_at_53411af8; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_productattribute_created_at_53411af8 ON public.catalog_productattribute USING btree (created_at);


--
-- Name: catalog_productattribute_name_6fe00e8b_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_productattribute_name_6fe00e8b_like ON public.catalog_productattribute USING btree (name varchar_pattern_ops);


--
-- Name: catalog_productattribute_slug_7a29bcb7_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_productattribute_slug_7a29bcb7_like ON public.catalog_productattribute USING btree (slug varchar_pattern_ops);


--
-- Name: catalog_productimage_created_at_367e8076; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_productimage_created_at_367e8076 ON public.catalog_productimage USING btree (created_at);


--
-- Name: catalog_productimage_product_id_1f42dd8c; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_productimage_product_id_1f42dd8c ON public.catalog_productimage USING btree (product_id);


--
-- Name: catalog_productreview_created_at_4c042ca8; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_productreview_created_at_4c042ca8 ON public.catalog_productreview USING btree (created_at);


--
-- Name: catalog_productreview_is_approved_603661d9; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_productreview_is_approved_603661d9 ON public.catalog_productreview USING btree (is_approved);


--
-- Name: catalog_productreview_product_id_9407c0e9; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_productreview_product_id_9407c0e9 ON public.catalog_productreview USING btree (product_id);


--
-- Name: catalog_productreview_user_id_b8f95029; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_productreview_user_id_b8f95029 ON public.catalog_productreview USING btree (user_id);


--
-- Name: catalog_productvariant_created_at_525afd68; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_productvariant_created_at_525afd68 ON public.catalog_productvariant USING btree (created_at);


--
-- Name: catalog_productvariant_product_id_422f9d19; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_productvariant_product_id_422f9d19 ON public.catalog_productvariant USING btree (product_id);


--
-- Name: catalog_productvariant_sku_da81620a_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX catalog_productvariant_sku_da81620a_like ON public.catalog_productvariant USING btree (sku varchar_pattern_ops);


--
-- Name: content_banner_created_at_24680f0b; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX content_banner_created_at_24680f0b ON public.content_banner USING btree (created_at);


--
-- Name: content_banner_is_active_19606de5; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX content_banner_is_active_19606de5 ON public.content_banner USING btree (is_active);


--
-- Name: content_banner_location_89e633bd; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX content_banner_location_89e633bd ON public.content_banner USING btree (location);


--
-- Name: content_banner_location_89e633bd_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX content_banner_location_89e633bd_like ON public.content_banner USING btree (location varchar_pattern_ops);


--
-- Name: content_newslettersubscription_created_at_2580bf8b; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX content_newslettersubscription_created_at_2580bf8b ON public.content_newslettersubscription USING btree (created_at);


--
-- Name: content_newslettersubscription_email_ab9bfc1f_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX content_newslettersubscription_email_ab9bfc1f_like ON public.content_newslettersubscription USING btree (email varchar_pattern_ops);


--
-- Name: content_page_created_at_91c2ccd3; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX content_page_created_at_91c2ccd3 ON public.content_page USING btree (created_at);


--
-- Name: content_page_is_published_8d0a35a7; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX content_page_is_published_8d0a35a7 ON public.content_page USING btree (is_published);


--
-- Name: content_page_slug_d48c800c_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX content_page_slug_d48c800c_like ON public.content_page USING btree (slug varchar_pattern_ops);


--
-- Name: content_sitesetting_created_at_a32ed8d2; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX content_sitesetting_created_at_a32ed8d2 ON public.content_sitesetting USING btree (created_at);


--
-- Name: content_sitesetting_key_0508b562_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX content_sitesetting_key_0508b562_like ON public.content_sitesetting USING btree (key varchar_pattern_ops);


--
-- Name: core_auditlog_action_978477aa; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX core_auditlog_action_978477aa ON public.core_auditlog USING btree (action);


--
-- Name: core_auditlog_action_978477aa_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX core_auditlog_action_978477aa_like ON public.core_auditlog USING btree (action varchar_pattern_ops);


--
-- Name: core_auditlog_resource_type_cb47b03d; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX core_auditlog_resource_type_cb47b03d ON public.core_auditlog USING btree (resource_type);


--
-- Name: core_auditlog_resource_type_cb47b03d_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX core_auditlog_resource_type_cb47b03d_like ON public.core_auditlog USING btree (resource_type varchar_pattern_ops);


--
-- Name: core_auditlog_timestamp_c6ef4463; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX core_auditlog_timestamp_c6ef4463 ON public.core_auditlog USING btree ("timestamp");


--
-- Name: core_auditlog_user_id_3797aaab; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX core_auditlog_user_id_3797aaab ON public.core_auditlog USING btree (user_id);


--
-- Name: discounts_coupon_code_f0958380_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX discounts_coupon_code_f0958380_like ON public.discounts_coupon USING btree (code varchar_pattern_ops);


--
-- Name: discounts_coupon_created_at_6027ed69; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX discounts_coupon_created_at_6027ed69 ON public.discounts_coupon USING btree (created_at);


--
-- Name: discounts_coupon_is_active_f70e8c25; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX discounts_coupon_is_active_f70e8c25 ON public.discounts_coupon USING btree (is_active);


--
-- Name: discounts_couponredemption_coupon_id_79fb0ae6; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX discounts_couponredemption_coupon_id_79fb0ae6 ON public.discounts_couponredemption USING btree (coupon_id);


--
-- Name: discounts_couponredemption_created_at_26d8c3e4; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX discounts_couponredemption_created_at_26d8c3e4 ON public.discounts_couponredemption USING btree (created_at);


--
-- Name: discounts_couponredemption_order_id_b81e0bd1; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX discounts_couponredemption_order_id_b81e0bd1 ON public.discounts_couponredemption USING btree (order_id);


--
-- Name: discounts_couponredemption_order_id_b81e0bd1_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX discounts_couponredemption_order_id_b81e0bd1_like ON public.discounts_couponredemption USING btree (order_id varchar_pattern_ops);


--
-- Name: discounts_couponredemption_user_id_d1d15838; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX discounts_couponredemption_user_id_d1d15838 ON public.discounts_couponredemption USING btree (user_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: inventory_inventoryitem_created_at_5aba1a64; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX inventory_inventoryitem_created_at_5aba1a64 ON public.inventory_inventoryitem USING btree (created_at);


--
-- Name: inventory_inventoryitem_sku_9ccfd20b_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX inventory_inventoryitem_sku_9ccfd20b_like ON public.inventory_inventoryitem USING btree (sku varchar_pattern_ops);


--
-- Name: inventory_stockmovement_created_at_05b478ed; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX inventory_stockmovement_created_at_05b478ed ON public.inventory_stockmovement USING btree (created_at);


--
-- Name: inventory_stockmovement_inventory_item_id_b4825f9c; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX inventory_stockmovement_inventory_item_id_b4825f9c ON public.inventory_stockmovement USING btree (inventory_item_id);


--
-- Name: inventory_stockmovement_user_id_9fe5f98d; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX inventory_stockmovement_user_id_9fe5f98d ON public.inventory_stockmovement USING btree (user_id);


--
-- Name: inventory_stockreservation_created_at_f1993588; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX inventory_stockreservation_created_at_f1993588 ON public.inventory_stockreservation USING btree (created_at);


--
-- Name: inventory_stockreservation_inventory_item_id_d06471c1; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX inventory_stockreservation_inventory_item_id_d06471c1 ON public.inventory_stockreservation USING btree (inventory_item_id);


--
-- Name: inventory_stockreservation_is_released_bd40c130; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX inventory_stockreservation_is_released_bd40c130 ON public.inventory_stockreservation USING btree (is_released);


--
-- Name: inventory_stockreservation_reference_id_f2f456f8; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX inventory_stockreservation_reference_id_f2f456f8 ON public.inventory_stockreservation USING btree (reference_id);


--
-- Name: inventory_stockreservation_reference_id_f2f456f8_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX inventory_stockreservation_reference_id_f2f456f8_like ON public.inventory_stockreservation USING btree (reference_id varchar_pattern_ops);


--
-- Name: orders_order_created_at_20b8d253; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_order_created_at_20b8d253 ON public.orders_order USING btree (created_at);


--
-- Name: orders_order_email_79665695; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_order_email_79665695 ON public.orders_order USING btree (email);


--
-- Name: orders_order_email_79665695_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_order_email_79665695_like ON public.orders_order USING btree (email varchar_pattern_ops);


--
-- Name: orders_order_order_number_4e985f70_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_order_order_number_4e985f70_like ON public.orders_order USING btree (order_number varchar_pattern_ops);


--
-- Name: orders_order_status_445594e5; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_order_status_445594e5 ON public.orders_order USING btree (status);


--
-- Name: orders_order_status_445594e5_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_order_status_445594e5_like ON public.orders_order USING btree (status varchar_pattern_ops);


--
-- Name: orders_order_user_id_e9b59eb1; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_order_user_id_e9b59eb1 ON public.orders_order USING btree (user_id);


--
-- Name: orders_orderitem_created_at_9431be56; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_orderitem_created_at_9431be56 ON public.orders_orderitem USING btree (created_at);


--
-- Name: orders_orderitem_order_id_fe61a34d; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_orderitem_order_id_fe61a34d ON public.orders_orderitem USING btree (order_id);


--
-- Name: orders_orderitem_product_id_afe4254a; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_orderitem_product_id_afe4254a ON public.orders_orderitem USING btree (product_id);


--
-- Name: orders_orderstatushistory_changed_by_id_d823a516; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_orderstatushistory_changed_by_id_d823a516 ON public.orders_orderstatushistory USING btree (changed_by_id);


--
-- Name: orders_orderstatushistory_created_at_535f9788; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_orderstatushistory_created_at_535f9788 ON public.orders_orderstatushistory USING btree (created_at);


--
-- Name: orders_orderstatushistory_order_id_bf09a0e1; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_orderstatushistory_order_id_bf09a0e1 ON public.orders_orderstatushistory USING btree (order_id);


--
-- Name: orders_returnrequest_created_at_002e2058; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_returnrequest_created_at_002e2058 ON public.orders_returnrequest USING btree (created_at);


--
-- Name: orders_returnrequest_order_id_176addea; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_returnrequest_order_id_176addea ON public.orders_returnrequest USING btree (order_id);


--
-- Name: orders_returnrequest_user_id_38896318; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_returnrequest_user_id_38896318 ON public.orders_returnrequest USING btree (user_id);


--
-- Name: orders_shipment_created_at_e9b9b26d; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX orders_shipment_created_at_e9b9b26d ON public.orders_shipment USING btree (created_at);


--
-- Name: payments_payment_created_at_149046d5; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_payment_created_at_149046d5 ON public.payments_payment USING btree (created_at);


--
-- Name: payments_payment_gateway_order_id_ebd789c6; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_payment_gateway_order_id_ebd789c6 ON public.payments_payment USING btree (gateway_order_id);


--
-- Name: payments_payment_gateway_order_id_ebd789c6_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_payment_gateway_order_id_ebd789c6_like ON public.payments_payment USING btree (gateway_order_id varchar_pattern_ops);


--
-- Name: payments_payment_status_fc8cbda2; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_payment_status_fc8cbda2 ON public.payments_payment USING btree (status);


--
-- Name: payments_payment_status_fc8cbda2_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_payment_status_fc8cbda2_like ON public.payments_payment USING btree (status varchar_pattern_ops);


--
-- Name: payments_payment_transaction_id_55f6af3a_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_payment_transaction_id_55f6af3a_like ON public.payments_payment USING btree (transaction_id varchar_pattern_ops);


--
-- Name: payments_paymentattempt_created_at_92b002cb; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_paymentattempt_created_at_92b002cb ON public.payments_paymentattempt USING btree (created_at);


--
-- Name: payments_paymentattempt_gateway_order_id_a70e0911; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_paymentattempt_gateway_order_id_a70e0911 ON public.payments_paymentattempt USING btree (gateway_order_id);


--
-- Name: payments_paymentattempt_gateway_order_id_a70e0911_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_paymentattempt_gateway_order_id_a70e0911_like ON public.payments_paymentattempt USING btree (gateway_order_id varchar_pattern_ops);


--
-- Name: payments_paymentattempt_order_id_d21442a3; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_paymentattempt_order_id_d21442a3 ON public.payments_paymentattempt USING btree (order_id);


--
-- Name: payments_paymentwebhookevent_created_at_7bbd1526; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_paymentwebhookevent_created_at_7bbd1526 ON public.payments_paymentwebhookevent USING btree (created_at);


--
-- Name: payments_paymentwebhookevent_event_id_4ef43bcf_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_paymentwebhookevent_event_id_4ef43bcf_like ON public.payments_paymentwebhookevent USING btree (event_id varchar_pattern_ops);


--
-- Name: payments_paymentwebhookevent_event_type_81be5efa; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_paymentwebhookevent_event_type_81be5efa ON public.payments_paymentwebhookevent USING btree (event_type);


--
-- Name: payments_paymentwebhookevent_event_type_81be5efa_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_paymentwebhookevent_event_type_81be5efa_like ON public.payments_paymentwebhookevent USING btree (event_type varchar_pattern_ops);


--
-- Name: payments_paymentwebhookevent_is_processed_7f28835a; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_paymentwebhookevent_is_processed_7f28835a ON public.payments_paymentwebhookevent USING btree (is_processed);


--
-- Name: payments_refundtransaction_created_at_816a1611; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_refundtransaction_created_at_816a1611 ON public.payments_refundtransaction USING btree (created_at);


--
-- Name: payments_refundtransaction_initiated_by_id_43c3e590; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_refundtransaction_initiated_by_id_43c3e590 ON public.payments_refundtransaction USING btree (initiated_by_id);


--
-- Name: payments_refundtransaction_payment_id_fd241ffa; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_refundtransaction_payment_id_fd241ffa ON public.payments_refundtransaction USING btree (payment_id);


--
-- Name: payments_refundtransaction_refund_id_a4cbbb91_like; Type: INDEX; Schema: public; Owner: ZIYO
--

CREATE INDEX payments_refundtransaction_refund_id_a4cbbb91_like ON public.payments_refundtransaction USING btree (refund_id varchar_pattern_ops);


--
-- Name: accounts_customeraddress accounts_customeraddress_user_id_09d750f6_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_customeraddress
    ADD CONSTRAINT accounts_customeraddress_user_id_09d750f6_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_user_groups accounts_user_groups_group_id_bd11a704_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_user_groups
    ADD CONSTRAINT accounts_user_groups_group_id_bd11a704_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_user_groups accounts_user_groups_user_id_52b62117_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_user_groups
    ADD CONSTRAINT accounts_user_groups_user_id_52b62117_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_user_user_permissions accounts_user_user_p_permission_id_113bb443_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_user_user_permissions
    ADD CONSTRAINT accounts_user_user_p_permission_id_113bb443_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_user_user_permissions accounts_user_user_p_user_id_e4f0a161_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_user_user_permissions
    ADD CONSTRAINT accounts_user_user_p_user_id_e4f0a161_fk_accounts_ FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_userprofile accounts_userprofile_user_id_92240672_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.accounts_userprofile
    ADD CONSTRAINT accounts_userprofile_user_id_92240672_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cart_cart cart_cart_user_id_9b4220b9_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_cart
    ADD CONSTRAINT cart_cart_user_id_9b4220b9_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cart_cartitem cart_cartitem_cart_id_370ad265_fk_cart_cart_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_cartitem
    ADD CONSTRAINT cart_cartitem_cart_id_370ad265_fk_cart_cart_id FOREIGN KEY (cart_id) REFERENCES public.cart_cart(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cart_cartitem cart_cartitem_product_id_b24e265a_fk_catalog_product_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_cartitem
    ADD CONSTRAINT cart_cartitem_product_id_b24e265a_fk_catalog_product_id FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cart_cartitem cart_cartitem_variant_id_69f5d8c8_fk_catalog_productvariant_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_cartitem
    ADD CONSTRAINT cart_cartitem_variant_id_69f5d8c8_fk_catalog_productvariant_id FOREIGN KEY (variant_id) REFERENCES public.catalog_productvariant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cart_wishlist cart_wishlist_user_id_c35eec54_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_wishlist
    ADD CONSTRAINT cart_wishlist_user_id_c35eec54_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cart_wishlistitem cart_wishlistitem_product_id_c183b0d4_fk_catalog_product_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_wishlistitem
    ADD CONSTRAINT cart_wishlistitem_product_id_c183b0d4_fk_catalog_product_id FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cart_wishlistitem cart_wishlistitem_wishlist_id_dd2c2649_fk_cart_wishlist_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.cart_wishlistitem
    ADD CONSTRAINT cart_wishlistitem_wishlist_id_dd2c2649_fk_cart_wishlist_id FOREIGN KEY (wishlist_id) REFERENCES public.cart_wishlist(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_category catalog_category_parent_id_f61bd017_fk_catalog_category_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_category
    ADD CONSTRAINT catalog_category_parent_id_f61bd017_fk_catalog_category_id FOREIGN KEY (parent_id) REFERENCES public.catalog_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_product catalog_product_category_id_35bf920b_fk_catalog_category_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_product
    ADD CONSTRAINT catalog_product_category_id_35bf920b_fk_catalog_category_id FOREIGN KEY (category_id) REFERENCES public.catalog_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_productimage catalog_productimage_product_id_1f42dd8c_fk_catalog_product_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_productimage
    ADD CONSTRAINT catalog_productimage_product_id_1f42dd8c_fk_catalog_product_id FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_productreview catalog_productreview_product_id_9407c0e9_fk_catalog_product_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_productreview
    ADD CONSTRAINT catalog_productreview_product_id_9407c0e9_fk_catalog_product_id FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_productreview catalog_productreview_user_id_b8f95029_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_productreview
    ADD CONSTRAINT catalog_productreview_user_id_b8f95029_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: catalog_productvariant catalog_productvaria_product_id_422f9d19_fk_catalog_p; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.catalog_productvariant
    ADD CONSTRAINT catalog_productvaria_product_id_422f9d19_fk_catalog_p FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_auditlog core_auditlog_user_id_3797aaab_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.core_auditlog
    ADD CONSTRAINT core_auditlog_user_id_3797aaab_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: discounts_couponredemption discounts_couponrede_coupon_id_79fb0ae6_fk_discounts; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.discounts_couponredemption
    ADD CONSTRAINT discounts_couponrede_coupon_id_79fb0ae6_fk_discounts FOREIGN KEY (coupon_id) REFERENCES public.discounts_coupon(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: discounts_couponredemption discounts_couponredemption_user_id_d1d15838_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.discounts_couponredemption
    ADD CONSTRAINT discounts_couponredemption_user_id_d1d15838_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: inventory_inventoryitem inventory_inventoryi_product_id_78574124_fk_catalog_p; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.inventory_inventoryitem
    ADD CONSTRAINT inventory_inventoryi_product_id_78574124_fk_catalog_p FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: inventory_inventoryitem inventory_inventoryi_variant_id_aa173510_fk_catalog_p; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.inventory_inventoryitem
    ADD CONSTRAINT inventory_inventoryi_variant_id_aa173510_fk_catalog_p FOREIGN KEY (variant_id) REFERENCES public.catalog_productvariant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: inventory_stockmovement inventory_stockmovem_inventory_item_id_b4825f9c_fk_inventory; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.inventory_stockmovement
    ADD CONSTRAINT inventory_stockmovem_inventory_item_id_b4825f9c_fk_inventory FOREIGN KEY (inventory_item_id) REFERENCES public.inventory_inventoryitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: inventory_stockmovement inventory_stockmovement_user_id_9fe5f98d_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.inventory_stockmovement
    ADD CONSTRAINT inventory_stockmovement_user_id_9fe5f98d_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: inventory_stockreservation inventory_stockreser_inventory_item_id_d06471c1_fk_inventory; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.inventory_stockreservation
    ADD CONSTRAINT inventory_stockreser_inventory_item_id_d06471c1_fk_inventory FOREIGN KEY (inventory_item_id) REFERENCES public.inventory_inventoryitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_order orders_order_user_id_e9b59eb1_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_user_id_e9b59eb1_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_orderitem orders_orderitem_order_id_fe61a34d_fk_orders_order_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_orderitem
    ADD CONSTRAINT orders_orderitem_order_id_fe61a34d_fk_orders_order_id FOREIGN KEY (order_id) REFERENCES public.orders_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_orderitem orders_orderitem_product_id_afe4254a_fk_catalog_product_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_orderitem
    ADD CONSTRAINT orders_orderitem_product_id_afe4254a_fk_catalog_product_id FOREIGN KEY (product_id) REFERENCES public.catalog_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_orderstatushistory orders_orderstatushi_changed_by_id_d823a516_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_orderstatushistory
    ADD CONSTRAINT orders_orderstatushi_changed_by_id_d823a516_fk_accounts_ FOREIGN KEY (changed_by_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_orderstatushistory orders_orderstatushistory_order_id_bf09a0e1_fk_orders_order_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_orderstatushistory
    ADD CONSTRAINT orders_orderstatushistory_order_id_bf09a0e1_fk_orders_order_id FOREIGN KEY (order_id) REFERENCES public.orders_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_returnrequest orders_returnrequest_order_id_176addea_fk_orders_order_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_returnrequest
    ADD CONSTRAINT orders_returnrequest_order_id_176addea_fk_orders_order_id FOREIGN KEY (order_id) REFERENCES public.orders_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_returnrequest orders_returnrequest_user_id_38896318_fk_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_returnrequest
    ADD CONSTRAINT orders_returnrequest_user_id_38896318_fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_shipment orders_shipment_order_id_661ed8ed_fk_orders_order_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.orders_shipment
    ADD CONSTRAINT orders_shipment_order_id_661ed8ed_fk_orders_order_id FOREIGN KEY (order_id) REFERENCES public.orders_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: payments_payment payments_payment_order_id_22c479b7_fk_orders_order_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.payments_payment
    ADD CONSTRAINT payments_payment_order_id_22c479b7_fk_orders_order_id FOREIGN KEY (order_id) REFERENCES public.orders_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: payments_paymentattempt payments_paymentattempt_order_id_d21442a3_fk_orders_order_id; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.payments_paymentattempt
    ADD CONSTRAINT payments_paymentattempt_order_id_d21442a3_fk_orders_order_id FOREIGN KEY (order_id) REFERENCES public.orders_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: payments_refundtransaction payments_refundtrans_initiated_by_id_43c3e590_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.payments_refundtransaction
    ADD CONSTRAINT payments_refundtrans_initiated_by_id_43c3e590_fk_accounts_ FOREIGN KEY (initiated_by_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: payments_refundtransaction payments_refundtrans_payment_id_fd241ffa_fk_payments_; Type: FK CONSTRAINT; Schema: public; Owner: ZIYO
--

ALTER TABLE ONLY public.payments_refundtransaction
    ADD CONSTRAINT payments_refundtrans_payment_id_fd241ffa_fk_payments_ FOREIGN KEY (payment_id) REFERENCES public.payments_payment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict 3poeeSsl6IaWO3TNMf8pLtoeiyyzIX9bmcDUb0ij7zL5MNSLF7oR5uXwr2Cx9kw

