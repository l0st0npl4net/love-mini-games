-- TSerial for Mr. Rescue on love-mini: tables to Lua text and back, as the game uses
-- them (its settings, high scores and statistics). This catalog's own (MIT), in place of
-- the game's TSerial.lua, which has no license.
TSerial = {}

local function key(k)
  if type(k) == "string" and k:match("^[%a_][%w_]*$") then return k end
  return "[" .. TSerial.value(k) .. "]"
end

function TSerial.value(v)
  local t = type(v)
  if t == "table" then return TSerial.pack(v) end
  if t == "string" then return string.format("%q", v) end
  if t == "number" or t == "boolean" then return tostring(v) end
  return "nil"
end

function TSerial.pack(t)
  local parts = {}
  for k, v in pairs(t) do
    if type(v) ~= "function" and type(v) ~= "userdata" then parts[#parts + 1] = key(k) .. "=" .. TSerial.value(v) end
  end
  return "{" .. table.concat(parts, ",") .. "}"
end

function TSerial.unpack(s)
  local f = loadstring("return " .. s)
  if not f then return nil end
  setfenv(f, {})
  local ok, t = pcall(f)
  if ok then return t end
end

return TSerial
