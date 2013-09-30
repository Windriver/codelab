<?php
// Copyright 2013, Not All Rights Reserved.
// Author:   Windriver
// Email:    windriver1986@gmail.com
// Created:  2013-09-30 23:37
//
// Description: Chapter1: PHP Crash Course

echo "\n";

echo "1.String Concatenation\n";
$str1 = "Hello";
$str2 = "world";
echo $str1 . ' ' . $str2 . "\n";
echo "\n";

echo "2.Type Castring\n";
$int1 = 2003;
echo gettype($int1) . "\n";
$float1 = (float)$int1;
echo gettype($float1) . "\n";
echo "\n";

echo "3.Declare Constants\n";
define ('CONST_INT', 9999);
echo CONST_INT . "\n";
define ('CONST_STR', 'Blue Cat');
echo CONST_STR . "\n";
echo "\n";

echo "4.Reference Operator\n";
$a = 5;
$b = &$a;
echo $a . "vs" . $b . "\n";
$b = 10;
echo $a . "vs" . $b . "\n";
unset($a);
echo "\n";

echo "5.Type Operator: instanceof\n";
class SampleClass{};
$object1 = new SampleClass();
if ($object1 instanceof SampleClass)
    echo "object1 is an instance of SampleClass\n";
echo "\n";

echo "6.Testing and Setting Variable Types\n";
$var1 = 100;
echo gettype($var1) . "\n";
settype($var1, 'double');
echo gettype($var1) . "\n";
echo "\n";

?>

