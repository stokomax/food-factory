/*
 * Biscuit.h
 *
 *  Created on: Mar 10, 2021
 *      Author: som
 */

#ifndef BISCUIT_H_
#define BISCUIT_H_

#include "Food.h"

class Biscuit: public Food {
public:
    Biscuit();
    string getName();
    ~Biscuit();
};

#endif /* BISCUIT_H_ */
