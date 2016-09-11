#!/usr/bin/gnuplot

set logscale y
set title "Residuals"
set ylabel 'Residual'
set xlabel 'Iteration'
plot "< cat log | grep 'Solving for Ux' | cut -d' ' -f9 | tr -d ','" title 'Ux' with lines,\
"< cat log | grep 'Solving for Uy' | cut -d' ' -f9 | tr -d ','" title 'Uy' with lines,\
"< cat log | grep 'Solving for Uz' | cut -d' ' -f9 | tr -d ','" title 'Uz' with lines,\
"< cat log | grep 'Solving for h' | cut -d' ' -f9 | tr -d ','" title 'h' with lines,\
"< cat log | grep 'Solving for epsilon' | cut -d' ' -f9 | tr -d ','" title 'epsilon' with lines,\
"< cat log | grep 'Solving for k' | cut -d' ' -f9 | tr -d ','" title 'k' with lines
pause 1
reread
