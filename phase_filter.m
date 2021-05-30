function P_out = phase_filter(P_in)
% Filter the phase 

mask = ones(3,3);

A = conv2(sin(P_in),mask,'same');
B = conv2(cos(P_in),mask,'same');

temp = atan2(A, B);
test = double(temp<0);
temp = temp + 2*pi.*double(temp<0);

P_out = temp;

end