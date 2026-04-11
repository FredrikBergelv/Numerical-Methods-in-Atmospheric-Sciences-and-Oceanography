program lec3
    implicit none

    integer :: n = 40

    print*, n, "!=", factorial(n)

    CONTAINS
    integer function factorial(n)
        implicit none
        integer :: n, ii, ifac = 1

        if (n==0 .or. n==1) then
            factorial = 1

        else if (n>1) then
            do ii=1, n
                ifac = ifac * ii
            end do
            factorial = ifac
        end if

    end function factorial


end program lec3