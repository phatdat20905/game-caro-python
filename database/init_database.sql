-- Database schema for Caro Game
-- SQLite version

-- User table
CREATE TABLE IF NOT EXISTS user (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Nickname VARCHAR(50) NOT NULL,
    Avatar VARCHAR(10) DEFAULT '0',
    NumberOfGame INTEGER DEFAULT 0,
    NumberOfWin INTEGER DEFAULT 0,
    NumberOfDraw INTEGER DEFAULT 0,
    IsOnline INTEGER DEFAULT 0,  -- 0 = false, 1 = true
    IsPlaying INTEGER DEFAULT 0  -- 0 = false, 1 = true
);

-- Friend table
CREATE TABLE IF NOT EXISTS friend (
    ID_User1 INTEGER NOT NULL,
    ID_User2 INTEGER NOT NULL,
    PRIMARY KEY (ID_User1, ID_User2),
    FOREIGN KEY (ID_User1) REFERENCES user(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_User2) REFERENCES user(ID) ON DELETE CASCADE
);

-- Banned user table
CREATE TABLE IF NOT EXISTS banned_user (
    ID_User INTEGER PRIMARY KEY,
    BannedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Reason TEXT,
    FOREIGN KEY (ID_User) REFERENCES user(ID) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_username ON user(Username);
CREATE INDEX IF NOT EXISTS idx_user_online ON user(IsOnline);
CREATE INDEX IF NOT EXISTS idx_user_playing ON user(IsPlaying);
CREATE INDEX IF NOT EXISTS idx_friend_user1 ON friend(ID_User1);
CREATE INDEX IF NOT EXISTS idx_friend_user2 ON friend(ID_User2);

-- Insert default admin user (password: admin123)
INSERT OR IGNORE INTO user (Username, Password, Nickname, Avatar, NumberOfGame, NumberOfWin, NumberOfDraw)
VALUES ('admin', 'admin123', 'Administrator', '0', 0, 0, 0);

-- Insert some demo users for testing
INSERT OR IGNORE INTO user (Username, Password, Nickname, Avatar, NumberOfGame, NumberOfWin, NumberOfDraw)
VALUES 
    ('player1', 'pass123', 'Player One', '1', 10, 7, 1),
    ('player2', 'pass123', 'Player Two', '2', 15, 9, 2),
    ('player3', 'pass123', 'Player Three', '3', 20, 12, 3);
