CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS stock_prices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(16) NOT NULL,
    price NUMERIC(18,6),
    open_price NUMERIC(18,6),
    high_price NUMERIC(18,6),
    low_price NUMERIC(18,6),
    close_price NUMERIC(18,6),
    volume BIGINT,
    api_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    source VARCHAR(64),
    raw_json JSONB,
    UNIQUE (symbol, api_timestamp)
);

CREATE INDEX IF NOT EXISTS idx_stock_symbol_time 
ON stock_prices(symbol, api_timestamp);
