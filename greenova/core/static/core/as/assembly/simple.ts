// Simple AssemblyScript test file

/**
 * Add two numbers
 * @param a - First number
 * @param b - Second number
 * @returns Sum of a and b
 */
export function add(a: i32, b: i32): i32 {
  return a + b;
}

/**
 * Calculate factorial
 * @param n - Input number
 * @returns Factorial of n
 */
export function factorial(n: i32): i32 {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}

/**
 * Check if a year is a leap year
 * @param year - Year to check
 * @returns 1 if leap year, 0 otherwise
 */
export function isLeapYear(year: i32): i32 {
  if (year % 4 !== 0) return 0;
  if (year % 100 !== 0) return 1;
  if (year % 400 !== 0) return 0;
  return 1;
}
