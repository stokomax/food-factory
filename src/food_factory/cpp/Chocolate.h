
/*
 * Chocolate.h
 *
 *  Created on: Mar 10, 2021
 *      Author: som
 */

#ifndef CHOCOLATE_H_
#define CHOCOLATE_H_

#include <iostream>
#include "Food.h"

class Chocolate: public Food {
public:
    Chocolate();
    virtual ~Chocolate();
    string getName();
};


#endif /* CHOCOLATE_H_ */
