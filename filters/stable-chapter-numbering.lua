-- Keep LaTeX chapter counters aligned with stable C-numbers even while an
-- earlier manuscript is absent. HTML navigation is corrected post-render.

function Header(header)
  if not FORMAT:match("latex") or header.level ~= 1 then
    return nil
  end

  local number = header.identifier:match("^c(%d%d)$")
  if number == nil then
    return nil
  end

  local counter = tonumber(number) - 1
  return {
    pandoc.RawBlock(
      "latex",
      "\\setcounter{chapter}{" .. tostring(counter) .. "}"
    ),
    header
  }
end
