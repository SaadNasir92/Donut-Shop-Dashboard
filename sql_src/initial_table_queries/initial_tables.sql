
CREATE TABLE "dim_employees" (
    "employee_id" INTEGER   NOT NULL,
    "employee_name" VARCHAR(100)   NOT NULL,
    "job_title" VARCHAR(30)   NOT NULL,
    CONSTRAINT "pk_dim_employees" PRIMARY KEY (
        "employee_id"
     )
);

CREATE TABLE "dim_dates" (
    "date_id" INTEGER   NOT NULL,
    "full_date" DATE   NOT NULL,
    "year" INTEGER   NOT NULL,
    "month" INTEGER   NOT NULL,
    "day" INTEGER   NOT NULL,
    "quarter" INTEGER   NOT NULL,
    CONSTRAINT "pk_dim_dates" PRIMARY KEY (
        "date_id"
     )
);

CREATE TABLE "dim_payment_methods" (
    "payment_method_id" INTEGER   NOT NULL,
    "payment_method" VARCHAR(10)   NOT NULL,
    CONSTRAINT "pk_dim_payment_methods" PRIMARY KEY (
        "payment_method_id"
     )
);

CREATE TABLE "dim_promotions" (
    "promotion_id" INTEGER   NOT NULL,
    "promotion_name" VARCHAR(50)   NOT NULL,
    "discount_percentage" DECIMAL(5,2)   NOT NULL,
    "description" VARCHAR(255)   NOT NULL,
    CONSTRAINT "pk_dim_promotions" PRIMARY KEY (
        "promotion_id"
     )
);

CREATE TABLE "dim_products" (
    "product_key" INTEGER   NOT NULL,
    "product_id" INTEGER   NOT NULL,
    "product_name" VARCHAR(50)   NOT NULL,
    "product_category" VARCHAR(50)   NOT NULL,
    "product_price" DECIMAL(10,2)   NOT NULL,
    "product_cost" DECIMAL(10,2)   NOT NULL,
    "start_date" DATE   NOT NULL,
    "end_date" DATE   NOT NULL,
    "is_current" Bool   NOT NULL,
    CONSTRAINT "pk_dim_products" PRIMARY KEY (
        "product_key"
     )
);

CREATE TABLE "fact_transactions" (
    "transaction_key" INTEGER   NOT NULL,
    "transaction_id" INTEGER   NOT NULL,
    "employee_id" INTEGER   NOT NULL,
    "product_key" INTEGER   NOT NULL,
    "date_id" INTEGER   NOT NULL,
    "promotion_id" INTEGER   NOT NULL,
    "payment_method_id" INTEGER   NOT NULL,
    "quantity" INTEGER   NOT NULL,
    "discount_amount" DECIMAL(10,2)   NOT NULL,
    "subtotal_amount" DECIMAL(10,2)   NOT NULL,
    "tax_amount" DECIMAL(10,2)   NOT NULL,
    "total_sale_amount" DECIMAL(10,2)   NOT NULL,
    CONSTRAINT "pk_fact_transactions" PRIMARY KEY (
        "transaction_key"
     )
);

ALTER TABLE "fact_transactions" ADD CONSTRAINT "fk_fact_transactions_employee_id" FOREIGN KEY("employee_id")
REFERENCES "dim_employees" ("employee_id");

ALTER TABLE "fact_transactions" ADD CONSTRAINT "fk_fact_transactions_product_key" FOREIGN KEY("product_key")
REFERENCES "dim_products" ("product_key");

ALTER TABLE "fact_transactions" ADD CONSTRAINT "fk_fact_transactions_date_id" FOREIGN KEY("date_id")
REFERENCES "dim_dates" ("date_id");

ALTER TABLE "fact_transactions" ADD CONSTRAINT "fk_fact_transactions_promotion_id" FOREIGN KEY("promotion_id")
REFERENCES "dim_promotions" ("promotion_id");

ALTER TABLE "fact_transactions" ADD CONSTRAINT "fk_fact_transactions_payment_method_id" FOREIGN KEY("payment_method_id")
REFERENCES "dim_payment_methods" ("payment_method_id");

