program lec3
    implicit none

    integer :: n = 6, result

    CALL factorial(n, result)

    print*, n, "!=", result

    CONTAINS
    SUBROUTINE factorial(arg1, arg2)
        implicit none
        integer :: ii
        integer, INTENT(in) :: arg1
        integer, INTENT(out) :: arg1

        arg = 1
        if (arg>1) then
            do ii=1, arg1
                arg2 = arg2 * ii
            end do
        end if



    END SUBROUTINE

end program lec3