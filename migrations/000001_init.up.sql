CREATE TABLE IF NOT EXISTS public.users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS public.images (
    id TEXT PRIMARY KEY,
    owner_id INTEGER REFERENCES users(id),
    private BOOLEAN,
    created_at TIMESTAMP without time zone DEFAULT now()
);
