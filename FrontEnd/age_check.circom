pragma circom 2.0.0;

// MODIFIED: This now includes the local comparators file
include "comparators.circom";

template AgeCheck() {
   // Private input: the user's secret age
   signal input age;

   // Public output: will be 1 if age is >= 18, otherwise 0
   signal output isOver18;

   // We want to prove that age >= 18, which is the same as 17 < age
   component isLessThan = LessThan(32); // Use a 32-bit comparator
   isLessThan.in[0] <== 17;
   isLessThan.in[1] <== age;

   // The output of LessThan is 1 if in[0] < in[1], so this works for our check
   isOver18 <== isLessThan.out;
}

// Instantiate the main component
component main = AgeCheck();