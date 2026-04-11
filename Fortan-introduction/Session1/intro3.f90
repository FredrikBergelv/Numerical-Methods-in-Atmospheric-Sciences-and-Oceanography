program lec_01
    implicit none

    ! Declaration of variables
    integer :: ii, isum

    ! Initialization
    isum = 0

    ! Do block
    ! sum all of even numbers between ___ and ___
    do ii=1,1000000,1
        isum=isum+ii
        !print*, "adding:", ii
    end do 

    print*, "The sum is:", isum

end program lec_01

