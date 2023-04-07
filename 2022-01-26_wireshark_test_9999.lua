p_test_9999 = Proto("TEST_PROTOCOL_9999", "My TEST Port 9999 Protocol")

local f_test_9999 = p_test_9999.fields
f_test_9999.ip_count = ProtoField.uint32("test.ip_count", "IP COUNT", base.DEC)
f_test_9999.ip0  = ProtoField.ipv4("test.ip0",  "IP 0")
f_test_9999.ip1  = ProtoField.ipv4("test.ip1",  "IP 1")
f_test_9999.ip2  = ProtoField.ipv4("test.ip2",  "IP 2")
f_test_9999.ip3  = ProtoField.ipv4("test.ip3",  "IP 3")
f_test_9999.ip4  = ProtoField.ipv4("test.ip4",  "IP 4")
f_test_9999.ip5  = ProtoField.ipv4("test.ip5",  "IP 5")
f_test_9999.ip6  = ProtoField.ipv4("test.ip6",  "IP 6")
f_test_9999.ip7  = ProtoField.ipv4("test.ip7",  "IP 7")
f_test_9999.ip8  = ProtoField.ipv4("test.ip8",  "IP 8")
f_test_9999.ip9  = ProtoField.ipv4("test.ip9",  "IP 9")
f_test_9999.ip10 = ProtoField.ipv4("test.ip10", "IP 10")
f_test_9999.ip11 = ProtoField.ipv4("test.ip11", "IP 11")
f_test_9999.ip12 = ProtoField.ipv4("test.ip12", "IP 12")
f_test_9999.ip13 = ProtoField.ipv4("test.ip13", "IP 13")
f_test_9999.ip14 = ProtoField.ipv4("test.ip14", "IP 14")
f_test_9999.ip15 = ProtoField.ipv4("test.ip15", "IP 15")
f_test_9999.ip16 = ProtoField.ipv4("test.ip16", "IP 16")

function p_test_9999.dissector (buffer, pinfo, tree)
  if buffer:len() == 0 then return end

  local ip_count = buffer(0, 4):le_uint()
  local ip_array = {}
  local ip_field_array = {f_test_9999.ip0
	, f_test_9999.ip1
	, f_test_9999.ip2
	, f_test_9999.ip3
	, f_test_9999.ip4
	, f_test_9999.ip5
	, f_test_9999.ip6
	, f_test_9999.ip7
	, f_test_9999.ip8
	, f_test_9999.ip9
	, f_test_9999.ip10
	, f_test_9999.ip11
	, f_test_9999.ip12
	, f_test_9999.ip13
	, f_test_9999.ip14
	, f_test_9999.ip15
	, f_test_9999.ip16}

  local info_str = "";
  info_str = info_str.."count="..ip_count
  
  subtree = tree:add(p_test_9999, buffer(0))
  subtree:add(f_test_9999.ip_count, ip_count)
  
  for index=1, ip_count do
	ip_array[index] = buffer(4 + (index - 1) * 4, 4)
	subtree:add_le(ip_field_array[index], ip_array[index])
	if index < 10 then
	  info_str = info_str.." ip"..(index-1).."="..tostring(buffer(4 + (index - 1) * 4, 4):le_ipv4())
	end
  end

  
  pinfo.cols.info = info_str
  pinfo.cols.protocol = p_test_9999.name
  --------------------------------------------------------
end

function p_test_9999.init()
end


local udp_dissector_table = DissectorTable.get("udp.port")
udp_dissector_table:add(9999, p_test_9999)
