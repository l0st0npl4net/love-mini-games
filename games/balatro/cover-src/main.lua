-- Drawn by love-mini (its tools/run.sh: SIZE=320x240 EVERY=3 tools/run.sh <this folder> 3),
-- the frame saved as ../cover.png. The font path is relative to the run: copy
-- ../wrapper/fonts/Nunito-Black.ttf here as font.ttf to run it as it was made.
-- love-mini-games' own cover for Balatro: drawn here, nothing of the game's art
local big, small, mid
function love.load()
  big = love.graphics.newFont("font.ttf", 54)
  mid = love.graphics.newFont("font.ttf", 18)
  small = love.graphics.newFont("font.ttf", 12)
end

local function heart(x, y, s, r, g, b)
  love.graphics.setColor(r, g, b)
  love.graphics.circle("fill", x - s * 0.5, y, s * 0.55)
  love.graphics.circle("fill", x + s * 0.5, y, s * 0.55)
  love.graphics.polygon("fill", x - s * 1.02, y + s * 0.15, x + s * 1.02, y + s * 0.15, x, y + s * 1.35)
end
local function spade(x, y, s, r, g, b)
  love.graphics.setColor(r, g, b)
  love.graphics.circle("fill", x - s * 0.5, y + s * 0.4, s * 0.55)
  love.graphics.circle("fill", x + s * 0.5, y + s * 0.4, s * 0.55)
  love.graphics.polygon("fill", x - s * 1.02, y + s * 0.25, x + s * 1.02, y + s * 0.25, x, y - s * 0.95)
  love.graphics.polygon("fill", x, y + s * 0.3, x - s * 0.45, y + s * 1.25, x + s * 0.45, y + s * 1.25)
end

local function card(x, y, r, suit, label, red)
  love.graphics.push()
  love.graphics.translate(x, y)
  love.graphics.rotate(r)
  love.graphics.setColor(0, 0, 0, 0.35)
  love.graphics.rectangle("fill", -27, -37, 60, 82, 7, 7)
  love.graphics.setColor(0.98, 0.96, 0.92)
  love.graphics.rectangle("fill", -30, -41, 60, 82, 7, 7)
  local cr, cg, cb = 0.2, 0.24, 0.27
  if red then cr, cg, cb = 0.93, 0.27, 0.27 end
  love.graphics.setColor(cr, cg, cb)
  love.graphics.setLineWidth(2)
  love.graphics.rectangle("line", -26, -37, 52, 74, 5, 5)
  love.graphics.setFont(mid)
  love.graphics.print(label, -22, -36)
  suit(0, -4, 11, cr, cg, cb)
  love.graphics.pop()
end

function love.draw()
  local G = love.graphics
  -- a swirl of rings, red into blue
  G.clear(0.13, 0.16, 0.2)
  for i = 24, 1, -1 do
    local t = i / 24
    local a = math.sin(i * 0.7) * 0.5 + 0.5
    G.setColor(0.16 + 0.55 * t * a, 0.2 + 0.1 * t, 0.3 + 0.45 * (1 - a) * t, 1)
    G.circle("fill", 160 + math.cos(i * 0.5) * 6, 120 + math.sin(i * 0.5) * 6, 10 + i * 9)
  end
  card(92, 150, -0.32, heart, "A", true)
  card(160, 140, 0.0, spade, "K", false)
  card(228, 150, 0.32, heart, "Q", true)
  -- the name, with a shadow
  G.setFont(big)
  local name = "BALATRO"
  local w = big:getWidth(name)
  G.setColor(0.05, 0.06, 0.08, 0.8)
  G.print(name, 160 - w / 2 + 3, 10 + 3)
  G.setColor(1, 1, 1)
  G.print(name, 160 - w / 2, 10)
  G.setFont(small)
  local sub = "YOUR COPY, ON LOVE-MINI"
  G.setColor(0.05, 0.06, 0.08, 0.75)
  G.rectangle("fill", 160 - small:getWidth(sub) / 2 - 8, 214, small:getWidth(sub) + 16, 18, 4, 4)
  G.setColor(1, 0.86, 0.35)
  G.print(sub, 160 - small:getWidth(sub) / 2, 215)
end
