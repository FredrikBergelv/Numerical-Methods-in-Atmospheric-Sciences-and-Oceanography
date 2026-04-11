program trapezoidal
    implicit none

    ! Declaration of variables
    real, parameter :: upperbound=2, lowerbound=0, error=0.001
    integer :: steps, ii
    real :: sum, func_0, func_1, x, real_func, error_now, width

    ! Initialization
    width = 1.0
    error_now = 10.0

    ! Do a while loop for error
    do while (error_now > error)
        steps = int((upperbound-lowerbound) / width)
        sum = 0.0

        ! Another loop to sum
        do ii=0, steps-1
            x = lowerbound + ii * width
            func_0 = func(x)
            func_1 = func(x+width)
            sum = sum + (width/2) * (func_0+func_1)
        end do

        ! Evaluate
        real_func = analytical_solution(upperbound) - analytical_solution(lowerbound)
        error_now = abs(sum-real_func)

        ! Lower width if answer is not right
        width = width - error
    end do

    ! Print info if ok
    print*, "INTIAL CONDITIONS:"
    print*, "Upperbound:            ", upperbound
    print*, "Lowerbound:            ", lowerbound
    print*, "Analytic integral:      ", real_func
    print*, ""
    print*, "RESULT:"
    print*, "Trapezoidal integral:  ", sum
    print*, "Error:                ", error_now
    print*, "Width of each step:   ", width

    ! These are functions we use in the code above
    contains
        ! The function we want to integrate
        real function func(x)
            real, intent(in) :: x
            func = sqrt(x) / (x+1)
        end function func

        ! Function for the analytical solution: 
        real function analytical_solution(x)
            real, intent(in) :: x
            analytical_solution = 2*sqrt(x) - 2*atan(sqrt(x))
        end function analytical_solution

end program trapezoidal
